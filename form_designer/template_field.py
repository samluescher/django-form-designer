from django.db import models
from django import forms

class TemplateFormField(forms.CharField):

    def clean(self, value):
        """
        Validates that the input can be compiled as a template.
        """
        value = super(TemplateFormField, self).clean(value)
        from django.template import Template, TemplateSyntaxError
        try:
            Template(value)
        except TemplateSyntaxError, error:
            raise forms.ValidationError(error)
        return value

class TemplateCharField(models.CharField):

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': TemplateFormField}
        defaults.update(kwargs)
        return super(TemplateCharField, self).formfield(**defaults)

class TemplateTextField(models.TextField):

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': TemplateFormField}
        defaults.update(kwargs)
        return super(TemplateTextField, self).formfield(**defaults)
