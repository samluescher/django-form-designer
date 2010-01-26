# encoding=utf8
from django.http import HttpResponse
from form_designer.models import FormLog
from form_designer.admin import FormLogAdmin
from form_designer import app_settings
from django.utils.translation import ugettext as _
from form_designer.templatetags.friendly import friendly
import csv

# Returns a QuerySet with the same ordering and filtering like the one that would be visible in Django admin
def get_change_list_query_set(model_admin, model, request):
    from django.contrib import admin
    from django.contrib.admin.views.main import ChangeList
    a = model_admin(model, admin.site)
    cl = ChangeList(request, a.model, a.list_display, a.list_display_links, a.list_filter,
        a.date_hierarchy, a.search_fields, a.list_select_related, a.list_per_page, a.list_editable, a)
    return cl.get_query_set()

def export_csv(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+app_settings.get('FORM_DESIGNER_CSV_EXPORT_FILENAME')
    writer = csv.writer(response, delimiter=app_settings.get('FORM_DESIGNER_CSV_EXPORT_DELIMITER'))
    qs = get_change_list_query_set(FormLogAdmin, FormLog, request)
    
    from django.db.models import Count
    distinct_forms = qs.aggregate(Count('form_definition', distinct=True))['form_definition__count']
    
    include_created = app_settings.get('FORM_DESIGNER_CSV_EXPORT_INCLUDE_CREATED')
    include_pk = app_settings.get('FORM_DESIGNER_CSV_EXPORT_INCLUDE_PK')
    include_header = app_settings.get('FORM_DESIGNER_CSV_EXPORT_INCLUDE_HEADER') and distinct_forms == 1
    include_form = app_settings.get('FORM_DESIGNER_CSV_EXPORT_INCLUDE_FORM') and distinct_forms > 1

    if include_header:
        header = [] 
        if include_form:
            header.append(_('Form'))
        if include_created:
            header.append(_('Created'))
        if include_pk:
            header.append(_('ID'))
        for field in qs.all()[0].data:
            header.append(field['label'] if field['label'] else field['key'])
        writer.writerow(header)

    for entry in qs:
        row = []
        if include_form:
            row.append(entry.form_definition)
        if include_created:
            row.append(entry.created)
        if include_pk:
            row.append(entry.pk)
        for field in entry.data:
            value = friendly(field['value'])
            if not isinstance(value, basestring):
                value = unicode(value)
            value = value.encode(app_settings.get('FORM_DESIGNER_CSV_EXPORT_ENCODING'))
            row.append(value)
        writer.writerow(row)

    return response
