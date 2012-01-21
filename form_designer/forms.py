import os

from django import forms
from django.forms import widgets
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _

from form_designer import settings
from form_designer.models import FormDefinitionField, FormDefinition
from form_designer.uploads import clean_files
from form_designer.utils import get_class


class DesignedForm(forms.Form):

    def __init__(self, form_definition, initial_data=None, *args, **kwargs):
        super(DesignedForm, self).__init__(*args, **kwargs)
        self.file_fields = []
        for def_field in form_definition.formdefinitionfield_set.all():
            self.add_defined_field(def_field, initial_data)
        self.fields[form_definition.submit_flag_name] = forms.BooleanField(required=False, initial=1, widget=widgets.HiddenInput)

    def add_defined_field(self, def_field, initial_data=None):
        if initial_data and initial_data.has_key(def_field.name):
            if not def_field.field_class in ('django.forms.MultipleChoiceField', 'django.forms.ModelMultipleChoiceField'):
                def_field.initial = initial_data.get(def_field.name)
            else:
                def_field.initial = initial_data.getlist(def_field.name)
        field = get_class(def_field.field_class)(**def_field.get_form_field_init_args())
        self.fields[def_field.name] = field
        if isinstance(field, forms.FileField):
            self.file_fields.append(def_field)

    def clean(self):
        return clean_files(self)
        

class FormDefinitionFieldInlineForm(forms.ModelForm):
    class Meta:
        model = FormDefinitionField

    def clean_regex(self):
        if not self.cleaned_data['regex'] and self.cleaned_data.has_key('field_class') and self.cleaned_data['field_class'] in ('django.forms.RegexField',):
            raise forms.ValidationError(_('This field class requires a regular expression.'))
        return self.cleaned_data['regex']

    def clean_choice_model(self):
        if not self.cleaned_data['choice_model'] and self.cleaned_data.has_key('field_class') and self.cleaned_data['field_class'] in ('django.forms.ModelChoiceField', 'django.forms.ModelMultipleChoiceField'):
            raise forms.ValidationError(_('This field class requires a model.'))
        return self.cleaned_data['choice_model']


class FormDefinitionForm(forms.ModelForm):
    class Meta:
        model = FormDefinition

    def _media(self):
        js = []
        plugins = [
            'js/jquery-ui.js',
            'js/jquery-inline-positioning.js',
            'js/jquery-inline-rename.js',
            'js/jquery-inline-collapsible.js',
            'js/jquery-inline-fieldset-collapsible.js',
            'js/jquery-inline-prepopulate-label.js',
        ]
        if hasattr(django_settings, 'JQUERY_URL'):
            js.append(django_settings.JQUERY_URL)
        else:
            plugins = ['js/jquery.js'] + plugins
        js.extend(
            [os.path.join(settings.STATIC_URL, path) for path in plugins])
        return forms.Media(js=js)
    media = property(_media)
