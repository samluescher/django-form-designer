import os

from django import forms
from django.forms import widgets
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _

from form_designer import settings
from form_designer.models import get_class, FormDefinitionField, FormDefinition

class DesignedForm(forms.Form):
    def __init__(self, form_definition, initial_data=None, *args, **kwargs):
        super(DesignedForm, self).__init__(*args, **kwargs)
        for def_field in form_definition.formdefinitionfield_set.all():
            self.add_defined_field(def_field, initial_data)
        self.fields[form_definition.submit_flag_name] = forms.BooleanField(required=False, initial=1, widget=widgets.HiddenInput)

    def add_defined_field(self, def_field, initial_data=None):
        if initial_data and initial_data.has_key(def_field.name):
            if not def_field.field_class in ('django.forms.MultipleChoiceField', 'django.forms.ModelMultipleChoiceField'):
                def_field.initial = initial_data.get(def_field.name)
            else:
                def_field.initial = initial_data.getlist(def_field.name)
        self.fields[def_field.name] = get_class(def_field.field_class)(**def_field.get_form_field_init_args())


class FormDefinitionFieldInlineForm(forms.ModelForm):
    class Meta:
        model = FormDefinitionField

    def clean_choice_model(self):
        if not self.cleaned_data['choice_model'] and self.cleaned_data.has_key('field_class') and self.cleaned_data['field_class'] in ('django.forms.ModelChoiceField', 'django.forms.ModelMultipleChoiceField'):
            raise forms.ValidationError(_('This field class requires a model.'))
        return self.cleaned_data['choice_model']


class FormDefinitionForm(forms.ModelForm):
    class Meta:
        model = FormDefinition

    def _media(self):
        js = []
        if hasattr(django_settings, 'CMS_MEDIA_URL'):
            # Use jQuery bundled with django_cms if installed
            js.append(os.path.join(django_settings.CMS_MEDIA_URL, 'js/lib/jquery.js'))
        elif hasattr(django_settings, 'JQUERY_URL'):
            js.append(settings.MEDIA_URL + 'js/jquery.js')
        js.extend(
            ['%s%s' % (settings.MEDIA_URL, path) for path in (
                'js/jquery-ui.js',
                'js/jquery-inline-positioning.js',
                'js/jquery-inline-rename.js',
                'js/jquery-inline-collapsible.js',
                'js/jquery-inline-fieldset-collapsible.js',
                'js/jquery-inline-prepopulate-label.js',
            )])
        return forms.Media(js=js)
    media = property(_media)
