from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.db import models
from form_designer.models import FormDefinition
from django.utils.translation import ugettext as _
from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from form_designer import app_settings

class DesignedForm(forms.Form):
    def __init__(self, definition_fields, *args, **kwargs):
        super(DesignedForm, self).__init__(*args, **kwargs)
        for def_field in definition_fields:
            self.fields[def_field.name] = eval(def_field.field_class)(**def_field.get_form_field_init_args())

def process_form(request, form_definition, context={}, is_cms_plugin=False):
    success_message = form_definition.success_message or _('Thank you, the data was submitted successfully.')
    error_message = form_definition.error_message or _('The data could not be submitted, please try again.')
    definition_fields = form_definition.formdefinitionfield_set.all()

    message = None
    if request.method == 'POST': # If the form has been submitted...
        form = DesignedForm(definition_fields, request.POST)
        if form.is_valid():
            # Successful submission
            if 'django_notify' in settings.INSTALLED_APPS:
                request.notifications.success(success_message)
            else:
                message = success_message
            if form_definition.log_data:
                form_definition.log(form)
            if form_definition.mail_to:
                form_definition.send_mail(form)
            if form_definition.success_redirect and not is_cms_plugin:
                # TODO Redirection does not work for cms plugin
                return HttpResponseRedirect(form_definition.action or '?')
            if form_definition.success_clear:
                form = DesignedForm(definition_fields) # clear form
        else:
            if 'django_notify' in settings.INSTALLED_APPS:
                request.notifications.error(error_message)
            else:
                message = error_message
    else:
        if form_definition.allow_get_initial:
            for field in definition_fields:
                if field.name in request.GET.keys():
                    if not field.field_class in ('forms.MultipleChoiceField', 'forms.ModelMultipleChoiceField'):
                        field.initial = request.GET.get(field.name)
                    else:
                        field.initial = request.GET.getlist(field.name)
        form = DesignedForm(definition_fields, request.GET)

    context.update({
        'message': message,
        'form': form,
        'form_definition': form_definition
    })

    return context

def detail(request, object_name):
    form_definition = get_object_or_404(FormDefinition, name=object_name)
    result = process_form(request, form_definition)
    if isinstance(result, HttpResponseRedirect):
        return result
    else:
        result.update({
            'form_template': form_definition.form_template_name or app_settings.get('FORM_DESIGNER_DEFAULT_FORM_TEMPLATE')
        })
        return render_to_response('html/formdefinition/detail.html', result, context_instance=RequestContext(request))
