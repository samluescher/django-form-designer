import csv
from django.contrib import admin
from django.utils.translation import ugettext as _, ugettext_lazy
from django.conf.urls.defaults import patterns, url
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count
from django.http import HttpResponse
from django.utils.encoding import smart_unicode, smart_str

try:
    import xlwt
except ImportError:
    xlwt_installed = False
else:
    xlwt_installed = True

from form_designer.forms import FormDefinitionForm, FormDefinitionFieldInlineForm
from form_designer.models import FormDefinition, FormDefinitionField, FormLog
from form_designer import settings
from form_designer.templatetags.friendly import friendly

class FormDefinitionFieldInline(admin.StackedInline):
    form = FormDefinitionFieldInlineForm
    model = FormDefinitionField
    extra = 1
    fieldsets = [
        (_('Basic'), {'fields': ['name', 'field_class', 'required', 'initial']}),
        (_('Display'), {'fields': ['label', 'widget', 'help_text', 'position', 'include_result']}),
        (_('Text'), {'fields': ['max_length', 'min_length']}),
        (_('Numbers'), {'fields': ['max_value', 'min_value', 'max_digits', 'decimal_places']}),
        (_('Regex'), {'fields': ['regex']}),
        (_('Choices'), {'fields': ['choice_values', 'choice_labels']}),
        (_('Model Choices'), {'fields': ['choice_model', 'choice_model_empty_label']}),
    ]

class FormDefinitionAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Basic'), {'fields': ['name', 'require_hash', 'method', 'action', 'title', 'body']}),
        (_('Settings'), {'fields': ['allow_get_initial', 'log_data', 'success_redirect', 'success_clear', 'display_logged', 'save_uploaded_files'], 'classes': ['collapse']}),
        (_('Mail form'), {'fields': ['mail_to', 'mail_from', 'mail_subject', 'mail_uploaded_files'], 'classes': ['collapse']}),
        (_('Templates'), {'fields': ['message_template', 'form_template_name'], 'classes': ['collapse']}),
        (_('Messages'), {'fields': ['success_message', 'error_message', 'submit_label'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'title', 'method', 'count_fields')
    form = FormDefinitionForm
    inlines = [
        FormDefinitionFieldInline,
    ]

class FormLogAdmin(admin.ModelAdmin):
    list_display = ('form_no_link', 'created', 'id', 'data_html')
    list_filter = ('form_definition',)
    list_display_links = ()
    actions = ['export_csv']
    if xlwt_installed:
        actions.append('export_xls')

    # Disabling all edit links: Hack as found at http://stackoverflow.com/questions/1618728/disable-link-to-edit-object-in-djangos-admin-display-list-only
    def form_no_link(self, obj):
        return '<a>'+obj.form_definition.__unicode__()+'</a>'
    form_no_link.admin_order_field = 'form_definition'
    form_no_link.allow_tags = True
    form_no_link.short_description = _('Form')

    def get_urls(self):
        urls = patterns('',
            url(r'^export/csv/$', self.admin_site.admin_view(self.export_csv), name='form_designer_export_csv'),
        )
        if xlwt_installed:
            urls += patterns('',
                url(r'^export/xls/$', self.admin_site.admin_view(self.export_xls), name='form_designer_export_xls'),
            )
        return urls + super(FormLogAdmin, self).get_urls()

    def data_html(self, obj):
        return obj.form_definition.compile_message(obj.data, 'html/formdefinition/data_message.html')
    data_html.allow_tags = True
    data_html.short_description = _('Data')

    def get_change_list_query_set(self, request):
        cl = ChangeList(request, self.model, self.list_display, self.list_display_links, self.list_filter,
            self.date_hierarchy, self.search_fields, self.list_select_related, self.list_per_page, self.list_editable, self)
        return cl.get_query_set()

    def export_csv(self, request, queryset=None):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + settings.CSV_EXPORT_FILENAME
        writer = csv.writer(response, delimiter=settings.CSV_EXPORT_DELIMITER)
        if queryset is None:
            queryset = self.get_change_list_query_set(request)

        distinct_forms = queryset.aggregate(Count('form_definition', distinct=True))['form_definition__count']

        include_created = settings.CSV_EXPORT_INCLUDE_CREATED
        include_pk = settings.CSV_EXPORT_INCLUDE_PK
        include_header = settings.CSV_EXPORT_INCLUDE_HEADER and distinct_forms == 1
        include_form = settings.CSV_EXPORT_INCLUDE_FORM and distinct_forms > 1

        if include_header:
            header = []
            if include_form:
                header.append(_('Form'))
            if include_created:
                header.append(_('Created'))
            if include_pk:
                header.append(_('ID'))
            for field in queryset[0].data:
                header.append(field['label'] if field['label'] else field['key'])
            writer.writerow([smart_str(cell, encoding=settings.CSV_EXPORT_ENCODING) for cell in header])

        for entry in queryset:
            row = []
            if include_form:
                row.append(entry.form_definition)
            if include_created:
                row.append(entry.created)
            if include_pk:
                row.append(entry.pk)
            for field in entry.data:
                value = friendly(field['value'])
                row.append(smart_str(
                    value, encoding=settings.CSV_EXPORT_ENCODING))
            writer.writerow(row)
        return response
    export_csv.short_description = ugettext_lazy("Export selected %(verbose_name_plural)s as CSV")

    def export_xls(self, request, queryset=None):
        import xlwt

        response = HttpResponse(mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % unicode(self.model._meta.verbose_name_plural)
        wb = xlwt.Workbook()
        ws = wb.add_sheet(unicode(self.model._meta.verbose_name_plural))
        if queryset is None:
            queryset = self.get_change_list_query_set(request)

        distinct_forms = queryset.aggregate(Count('form_definition', distinct=True))['form_definition__count']

        include_created = settings.CSV_EXPORT_INCLUDE_CREATED
        include_pk = settings.CSV_EXPORT_INCLUDE_PK
        include_header = settings.CSV_EXPORT_INCLUDE_HEADER and distinct_forms == 1
        include_form = settings.CSV_EXPORT_INCLUDE_FORM and distinct_forms > 1

        if include_header:
            header = []
            if include_form:
                header.append(_('Form'))
            if include_created:
                header.append(_('Created'))
            if include_pk:
                header.append(_('ID'))
            for field in queryset[0].data:
                header.append(field['label'] if field['label'] else field['key'])
            for i, f in enumerate(header):
                ws.write(0, i, smart_unicode(f, encoding=settings.CSV_EXPORT_ENCODING))

        for i, entry in enumerate(queryset):
            row = []
            if include_form:
                row.append(entry.form_definition)
            if include_created:
                row.append(entry.created)
            if include_pk:
                row.append(entry.pk)
            for field in entry.data:
                value = friendly(field['value'])
                row.append(smart_unicode(
                    value, encoding=settings.CSV_EXPORT_ENCODING))
            for j, cell in enumerate(row):
                ws.write(i+1, j, smart_unicode(cell))
        wb.save(response)
        return response
    export_xls.short_description = ugettext_lazy("Export selected %(verbose_name_plural)s as XLS")

    def changelist_view(self, request, extra_context=None):
        from django.core.urlresolvers import reverse, NoReverseMatch
        extra_context = extra_context or {}
        try:
            query_string = '?'+request.META['QUERY_STRING']
        except (TypeError, KeyError):
            query_string = ''
        try:
            extra_context['export_csv_url'] = reverse('admin:form_designer_export_csv')+query_string
        except NoReverseMatch:
            request.user.message_set.create(message=_('CSV export is not enabled.'))
        if xlwt_installed:
            try:
                extra_context['export_xls_url'] = reverse('admin:form_designer_export_xls')+query_string
            except NoReverseMatch:
                request.user.message_set.create(message=_('XLS export is not enabled.'))
        return super(FormLogAdmin, self).changelist_view(request, extra_context)

admin.site.register(FormDefinition, FormDefinitionAdmin)
admin.site.register(FormLog, FormLogAdmin)
