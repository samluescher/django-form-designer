from django.contrib import admin
from form_designer.models import FormDefinition, FormDefinitionField, FormLog
from django import forms
from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings
import os

MEDIA_SUBDIR = 'form_designer'

class FormDefinitionFieldInlineForm(forms.ModelForm):
    class Meta:
        model = FormDefinitionField
        
    def clean_choice_model(self):
        if not self.cleaned_data['choice_model'] and self.cleaned_data.has_key('field_class') and self.cleaned_data['field_class'] in ('forms.ModelChoiceField', 'forms.ModelMultipleChoiceField'):
            raise forms.ValidationError(_('This field class requires a model.'))
        return self.cleaned_data['choice_model']

class FormDefinitionFieldInline(admin.StackedInline):
    form = FormDefinitionFieldInlineForm
    model = FormDefinitionField
    extra = 8
    fieldsets = [
        (_('Basic'), {'fields': ['name', 'field_class', 'required', 'initial']}),
        (_('Display'), {'fields': ['label', 'widget', 'help_text', 'position', 'include_result']}),
        (_('Text'), {'fields': ['max_length', 'min_length']}),
        (_('Numbers'), {'fields': ['max_value', 'min_value', 'max_digits', 'decimal_places']}),
        (_('Regex'), {'fields': ['regex']}),
        (_('Choices'), {'fields': ['choice_values', 'choice_labels']}),
        (_('Model Choices'), {'fields': ['choice_model', 'choice_model_empty_label']}),
    ]

class FormDefinitionForm(forms.ModelForm):
    class Meta:
        model = FormDefinition
    class Media:
        js = ([
                # Use central jQuery
                settings.JQUERY_JS,
                # and use jQuery UI bundled with this app
                os.path.join(MEDIA_SUBDIR, 'lib/jquery/ui.core.js'),
                os.path.join(MEDIA_SUBDIR, 'lib/jquery/ui.sortable.js'),
            ] if hasattr(settings, 'JQUERY_JS') else [
                # Use jQuery bundled with CMS
                os.path.join(settings.CMS_MEDIA_URL, 'js/lib/jquery.js'),
                os.path.join(settings.CMS_MEDIA_URL, 'js/lib/ui.core.js'),
                os.path.join(settings.CMS_MEDIA_URL, 'js/lib/ui.sortable.js'),
            ] if hasattr(settings, 'CMS_MEDIA_URL') else [
                # or use jQuery bundled with this app
                os.path.join(MEDIA_SUBDIR, 'lib/jquery/jquery.js'),
                os.path.join(MEDIA_SUBDIR, 'lib/jquery/ui.core.js'),
                os.path.join(MEDIA_SUBDIR, 'lib/jquery/ui.sortable.js'),
            ])+[os.path.join(MEDIA_SUBDIR, 'js/lib/django-admin-tweaks-js-lib/js', basename) for basename in (
                'jquery-inline-positioning.js',
                'jquery-inline-rename.js',
                'jquery-inline-collapsible.js',
                'jquery-inline-fieldset-collapsible.js',
                'jquery-inline-prepopulate-label.js',
            )]

class FormDefinitionAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Basic'), {'fields': ['name', 'method', 'action', 'title', 'allow_get_initial', 'log_data', 'success_redirect', 'success_clear']}),
        (_('Mail form'), {'fields': ['mail_to', 'mail_from', 'mail_subject'], 'classes': ['collapse']}),
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
    
    # Disabling all edit links: Hack as found at http://stackoverflow.com/questions/1618728/disable-link-to-edit-object-in-djangos-admin-display-list-only
    def form_no_link(self, obj):
        return '<a>'+obj.form_definition.__unicode__()+'</a>'
    form_no_link.admin_order_field = 'form_definition'
    form_no_link.allow_tags = True
    form_no_link.short_description = _('Form')

    def data_html(self, obj):
        return obj.form_definition.compile_message(obj.data, 'html/formdefinition/data_message.html')
    data_html.allow_tags = True
    data_html.short_description = _('Data')

    def changelist_view(self, request, extra_context=None):
        from django.core.urlresolvers import reverse, NoReverseMatch 
        extra_context = extra_context or {}
        try:
            query_string = '?'+request.META['QUERY_STRING']
        except TypeError, KeyError:
            query_string = ''
        try:
            extra_context['export_csv_url'] = reverse('form_designer_export_csv')+query_string
        except NoReverseMatch:
            request.user.message_set.create(message=_('CSV export is not enabled.'))
        
        return super(FormLogAdmin, self).changelist_view(request, extra_context)

admin.site.register(FormDefinition, FormDefinitionAdmin)
admin.site.register(FormLog, FormLogAdmin)

