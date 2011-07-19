from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.context_processors import csrf

import os
import random
from datetime import datetime

from form_designer.forms import DesignedForm
from form_designer.models import FormDefinition

def process_form(request, form_definition, context={}, is_cms_plugin=False):
    success_message = form_definition.success_message or _('Thank you, the data was submitted successfully.')
    error_message = form_definition.error_message or _('The data could not be submitted, please try again.')
    message = None
    form_error = False
    form_success = False
    is_submit = False
    # If the form has been submitted...
    if request.method == 'POST' and request.POST.get(form_definition.submit_flag_name):
        form = DesignedForm(form_definition, None, request.POST, request.FILES)
        is_submit = True
    if request.method == 'GET' and request.GET.get(form_definition.submit_flag_name):
        form = DesignedForm(form_definition, None, request.GET)
        is_submit = True

    if is_submit:
        if form.is_valid():
            # Handle file uploads
            files = []
            if hasattr(request, 'FILES'):
                for file_key in request.FILES:
                    file_obj = request.FILES[file_key]
                    file_name = '%s.%s_%s' % (
                        datetime.now().strftime('%Y%m%d'),
                        random.randrange(0, 10000),
                        file_obj.name,
                    )

                    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'contact_form')):
                        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'contact_form'))

                    destination = open(os.path.join(settings.MEDIA_ROOT, 'contact_form', file_name), 'wb+')
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                    destination.close()

                    form.cleaned_data[file_key] = os.path.join(settings.MEDIA_URL, 'contact_form', file_name)
                    files.append(os.path.join(settings.MEDIA_ROOT, 'contact_form', file_name))

            # Successful submission
            messages.success(request, success_message)
            message = success_message
            form_success = True
            if form_definition.log_data:
                form_definition.log(form)
            if form_definition.mail_to:
                form_definition.send_mail(form, files)
            if form_definition.success_redirect and not is_cms_plugin:
                # TODO Redirection does not work for cms plugin
                return HttpResponseRedirect(form_definition.action or '?')
            if form_definition.success_clear:
                form = DesignedForm(form_definition) # clear form
        else:
            form_error = True
            messages.error(request, error_message)
            message = error_message
    else:
        if form_definition.allow_get_initial:
            form = DesignedForm(form_definition, initial_data=request.GET)
        else:
            form = DesignedForm(form_definition)

    context.update({
        'message': message,
        'form_error': form_error,
        'form_success': form_success,
        'form': form,
        'form_definition': form_definition
    })
    context.update(csrf(request))
    return context

def detail(request, object_name):
    form_definition = get_object_or_404(FormDefinition, name=object_name)
    result = process_form(request, form_definition)
    if isinstance(result, HttpResponseRedirect):
        return result
    result.update({
        'form_template': form_definition.form_template_name or settings.DEFAULT_FORM_TEMPLATE
    })
    return render_to_response('html/formdefinition/detail.html', result,
        context_instance=RequestContext(request))
