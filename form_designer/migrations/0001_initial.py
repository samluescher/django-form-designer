# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import form_designer.fields
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FormDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, max_length=255, verbose_name='name')),
                ('require_hash', models.BooleanField(default=False, help_text='If enabled, the form can only be reached via a secret URL.', verbose_name='obfuscate URL to this form')),
                ('private_hash', models.CharField(default=b'', max_length=40, editable=False)),
                ('public_hash', models.CharField(default=b'', max_length=40, editable=False)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='title', blank=True)),
                ('body', models.TextField(null=True, verbose_name='body', blank=True)),
                ('action', models.URLField(help_text='If you leave this empty, the page where the form resides will be requested, and you can use the mail form and logging features. You can also send data to external sites: For instance, enter "http://www.google.ch/search" to create a search form.', max_length=255, null=True, verbose_name='target URL', blank=True)),
                ('mail_to', form_designer.fields.TemplateCharField(help_text=b'Separate several addresses with a comma. Your form fields are available as template context. Example: "admin@domain.com, {{ from_email }}" if you have a field named `from_email`.', max_length=255, null=True, verbose_name='send form data to e-mail address', blank=True)),
                ('mail_from', form_designer.fields.TemplateCharField(help_text=b'Your form fields are available as template context. Example: "{{ first_name }} {{ last_name }} <{{ from_email }}>" if you have fields named `first_name`, `last_name`, `from_email`.', max_length=255, null=True, verbose_name='sender address', blank=True)),
                ('mail_subject', form_designer.fields.TemplateCharField(help_text=b'Your form fields are available as template context. Example: "Contact form {{ subject }}" if you have a field named `subject`.', max_length=255, null=True, verbose_name='email subject', blank=True)),
                ('mail_uploaded_files', models.BooleanField(default=True, verbose_name='Send uploaded files as email attachments')),
                ('method', models.CharField(default=b'POST', max_length=10, verbose_name='method', choices=[(b'POST', b'POST'), (b'GET', b'GET')])),
                ('success_message', models.CharField(max_length=255, null=True, verbose_name='success message', blank=True)),
                ('error_message', models.CharField(max_length=255, null=True, verbose_name='error message', blank=True)),
                ('submit_label', models.CharField(max_length=255, null=True, verbose_name='submit button label', blank=True)),
                ('log_data', models.BooleanField(default=True, help_text='Logs all form submissions to the database.', verbose_name='log form data')),
                ('save_uploaded_files', models.BooleanField(default=True, help_text='Saves all uploaded files using server storage.', verbose_name='save uploaded files')),
                ('success_redirect', models.BooleanField(default=True, verbose_name='HTTP redirect after successful submission')),
                ('success_clear', models.BooleanField(default=True, verbose_name='clear form after successful submission')),
                ('allow_get_initial', models.BooleanField(default=True, help_text='If enabled, you can fill in form fields by adding them to the query string.', verbose_name='allow initial values via URL')),
                ('message_template', form_designer.fields.TemplateTextField(help_text='Your form fields are available as template context. Example: "{{ message }}" if you have a field named `message`. To iterate over all fields, use the variable `data` (a list containing a dictionary for each form field, each containing the elements `name`, `label`, `value`).', null=True, verbose_name='message template', blank=True)),
                ('form_template_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='form template', choices=[(b'', 'Default'), (b'html/formdefinition/forms/as_p.html', 'as paragraphs'), (b'html/formdefinition/forms/as_table.html', 'as table'), (b'html/formdefinition/forms/as_table_h.html', 'as table (horizontal)'), (b'html/formdefinition/forms/as_ul.html', 'as unordered list'), (b'html/formdefinition/forms/custom.html', 'custom implementation')])),
                ('display_logged', models.BooleanField(default=False, verbose_name='display logged submissions with form')),
            ],
            options={
                'verbose_name': 'Form',
                'verbose_name_plural': 'Forms',
            },
        ),
        migrations.CreateModel(
            name='FormDefinitionField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_class', models.CharField(max_length=100, verbose_name='field class', choices=[(b'django.forms.CharField', 'Text'), (b'django.forms.EmailField', 'E-mail address'), (b'django.forms.URLField', 'Web address'), (b'django.forms.IntegerField', 'Number'), (b'django.forms.DecimalField', 'Decimal number'), (b'django.forms.BooleanField', 'Yes/No'), (b'django.forms.DateField', 'Date'), (b'django.forms.DateTimeField', 'Date & time'), (b'django.forms.TimeField', 'Time'), (b'django.forms.ChoiceField', 'Choice'), (b'django.forms.MultipleChoiceField', 'Multiple Choice'), (b'django.forms.ModelChoiceField', 'Model Choice'), (b'django.forms.ModelMultipleChoiceField', 'Model Multiple Choice'), (b'django.forms.RegexField', 'Regex'), (b'django.forms.FileField', 'File')])),
                ('position', models.IntegerField(null=True, verbose_name='position', blank=True)),
                ('name', models.SlugField(max_length=255, verbose_name='name')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='label', blank=True)),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('include_result', models.BooleanField(default=True, help_text=b'If this is disabled, the field value will not be included in logs and e-mails generated from form data.', verbose_name='include in result')),
                ('widget', models.CharField(default=b'', choices=[(b'', 'Default'), (b'django.forms.widgets.Textarea', 'Text area'), (b'django.forms.widgets.PasswordInput', 'Password input'), (b'django.forms.widgets.HiddenInput', 'Hidden input'), (b'django.forms.widgets.RadioSelect', 'Radio button')], max_length=255, blank=True, null=True, verbose_name='widget')),
                ('initial', models.TextField(null=True, verbose_name='initial value', blank=True)),
                ('help_text', models.CharField(max_length=255, null=True, verbose_name='help text', blank=True)),
                ('choice_values', models.TextField(help_text='One value per line', null=True, verbose_name='values', blank=True)),
                ('choice_labels', models.TextField(help_text='One label per line', null=True, verbose_name='labels', blank=True)),
                ('max_length', models.IntegerField(null=True, verbose_name='max. length', blank=True)),
                ('min_length', models.IntegerField(null=True, verbose_name='min. length', blank=True)),
                ('max_value', models.FloatField(null=True, verbose_name='max. value', blank=True)),
                ('min_value', models.FloatField(null=True, verbose_name='min. value', blank=True)),
                ('max_digits', models.IntegerField(null=True, verbose_name='max. digits', blank=True)),
                ('decimal_places', models.IntegerField(null=True, verbose_name='decimal places', blank=True)),
                ('regex', form_designer.fields.RegexpExpressionField(max_length=255, null=True, verbose_name='regular Expression', blank=True)),
                ('choice_model', form_designer.fields.ModelNameField(help_text=b'your_app.models.ModelName', max_length=255, null=True, verbose_name='data model', blank=True)),
                ('choice_model_empty_label', models.CharField(max_length=255, null=True, verbose_name='empty label', blank=True)),
                ('form_definition', models.ForeignKey(to='form_designer.FormDefinition')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
        ),
        migrations.CreateModel(
            name='FormLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('form_definition', models.ForeignKey(related_name='logs', to='form_designer.FormDefinition')),
            ],
        ),
        migrations.CreateModel(
            name='FormValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_name', models.SlugField(max_length=255, verbose_name='field name')),
                ('value', picklefield.fields.PickledObjectField(verbose_name='value', null=True, editable=False, blank=True)),
                ('form_log', models.ForeignKey(related_name='values', to='form_designer.FormLog')),
            ],
        ),
    ]
