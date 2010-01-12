from django.db import models
from django import forms

class ModelNameFormField(forms.CharField):

    @staticmethod
    def get_model_from_string(model_path):
        try:
            app_label, model_name = model_path.rsplit('.models.')
            return models.get_model(app_label, model_name)
        except:
            return None

    def clean(self, value):
        """
        Validates that the input matches the regular expression. Returns a
        Unicode object.
        """
        value = super(ModelNameFormField, self).clean(value)
        if value == u'':
            return value
        if not ModelNameFormField.get_model_from_string(value):
            raise forms.ValidationError(self.error_messages['invalid'])
        return value

class ModelNameField(models.CharField):

    @staticmethod
    def get_model_from_string(model_path):
        return ModelNameFormField.get_model_from_string(model_path)
        
    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': ModelNameFormField}
        defaults.update(kwargs)
        return super(ModelNameField, self).formfield(**defaults)
