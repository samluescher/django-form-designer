from django.contrib import admin
from form_designer.models import FormDefinition, FormDefinitionField, FormLog
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

class FormDefinitionFieldInline(admin.StackedInline):
    model = FormDefinitionField
    extra = 8
    fieldsets = [
        (_('Basic'), {'fields': ['name', 'field_class', 'required', 'initial']}),
        (_('Display'), {'fields': ['label', 'widget', 'help_text', 'position']}),
        (_('Text'), {'fields': ['max_length', 'min_length']}),
        (_('Numbers'), {'fields': ['max_value', 'min_value', 'max_digits', 'decimal_places']}),
        (_('Regex'), {'fields': ['regex']}),
        (_('Choices'), {'fields': ['choice_values', 'choice_labels']}),
    ]

class FormDefinitionForm(forms.ModelForm):
    class Meta:
        model = FormDefinition
    class Media:
        # TODO use jQuery bundled with django_cms if installed  
        js = (
            'form_designer/js/lib/jquery.js' if not hasattr(settings, 'JQUERY_JS') else settings.JQUERY_JS,
            'form_designer/js/lib/jquery-ui.js' if not hasattr(settings, 'JQUERY_UI_JS') else settings.JQUERY_UI_JS,
            'form_designer/js/jquery-inline-rename.js',
            'form_designer/js/jquery-inline-positioning.js',
            'form_designer/js/jquery-inline-collapsible.js',
            'form_designer/js/jquery-inline-fieldset-collapsible.js',
            'form_designer/js/jquery-inline-prepopulate-label.js',
        )

    def validate_template(self, text):
        from django.template import Template, TemplateSyntaxError
        try:
            Template(text)
        except TemplateSyntaxError as error:
            raise forms.ValidationError(error)
        return text

    def clean_message_template(self):
        return self.validate_template(self.cleaned_data['message_template'])

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
    list_display = ('form_definition', 'created', 'data_html')
    list_filter = ('form_definition',)
    list_display_links = ()

admin.site.register(FormDefinition, FormDefinitionAdmin)
admin.site.register(FormLog, FormLogAdmin)

