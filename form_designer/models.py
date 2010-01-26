from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import widgets
from django.core.mail import send_mail
from django.conf import settings
from form_designer import app_settings
import re
from pickled_object_field import PickledObjectField
from model_name_field import ModelNameField
from template_field import TemplateTextField, TemplateCharField

class FormDefinition(models.Model):
    name = models.SlugField(_('Name'), max_length=255, unique=True)
    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    action = models.URLField(_('Target URL'), help_text=_('If you leave this empty, the page where the form resides will be requested, and you can use the mail form and logging features. You can also send data to external sites: For instance, enter "http://www.google.ch/search" to create a search form.'), max_length=255, blank=True, null=True)
    mail_to = TemplateCharField(_('Send form data to e-mail address'), help_text=('Separate several addresses with a comma. Your form fields are available as template context. Example: "admin@domain.com, {{ from_email }}" if you have a field named "from_email".'), max_length=255, blank=True, null=True)
    mail_from = TemplateCharField(_('Sender address'), max_length=255, help_text=('Your form fields are available as template context. Example: "{{ firstname }} {{ lastname }} <{{ from_email }}>" if you have fields named "first_name", "last_name", "from_email".'), blank=True, null=True)
    mail_subject = TemplateCharField(_('e-Mail subject'), max_length=255, help_text=('Your form fields are available as template context. Example: "Contact form {{ subject }}" if you have a field named "subject".'), blank=True, null=True)
    method = models.CharField(_('Method'), max_length=10, default="POST", choices = (('POST', 'POST'), ('GET', 'GET')))
    success_message = models.CharField(_('Success message'), max_length=255, blank=True, null=True)
    error_message = models.CharField(_('Error message'), max_length=255, blank=True, null=True)
    submit_label = models.CharField(_('Submit button label'), max_length=255, blank=True, null=True)
    log_data = models.BooleanField(_('Log form data'), help_text=_('Logs all form submissions to the database.'), default=True)
    success_redirect = models.BooleanField(_('Redirect after success'), help_text=_('You should install django_notify if you want to enable this.') if not 'django_notify' in settings.INSTALLED_APPS else None, default=False)
    success_clear = models.BooleanField(_('Clear form after success'), default=True)
    allow_get_initial = models.BooleanField(_('Allow initial values via URL'), help_text=_('If enabled, you can fill in form fields by adding them to the query string.'), default=True)
    message_template = TemplateTextField(_('Message template'), help_text=_('Available context: "data" (a list containing a dictionary for each form field, each containing the elements "name", "label", "value").'), blank=True, null=True)
    form_template_name = models.CharField(_('Form template'), max_length=255, choices=app_settings.get('FORM_DESIGNER_FORM_TEMPLATES'), blank=True, null=True)

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def get_field_dict(self):
        dict = {}
        for field in self.formdefinitionfield_set.all():
            dict[field.name] = field
        return dict
        
    def get_form_data(self, form):
        data = []
        field_dict = self.get_field_dict()
        form_keys = form.fields.keys()
        def_keys = field_dict.keys()
        for key in form_keys:
            if key in def_keys and field_dict[key].include_result:
                data.append({'name': key, 'label': form.fields[key].label, 'value': form.cleaned_data[key]})
        return data
        
    def get_form_data_dict(self, form_data):
        dict = {}
        for field in form_data:
            dict[field['name']] = field['value']
        return dict

    def compile_message(self, form_data, template=None):
        from django.template.loader import get_template
        from django.template import Context, Template
        if template:
            t = get_template(template)
        elif not self.message_template:
            t = get_template('txt/formdefinition/data_message.txt')
        else:
            t = Template(self.message_template)
        return t.render(Context({'data': form_data}))

    def count_fields(self):
        return self.formdefinitionfield_set.count()
    count_fields.short_description = _('Fields')

    def __unicode__(self):
        return self.title or self.name

    def log(self, form):
        FormLog(form_definition=self, data=self.get_form_data(form)).save()

    def string_template_replace(self, text, context_dict):
        from django.template import Context, Template, TemplateSyntaxError
        try:
            t = Template(text)
            return t.render(Context(context_dict))
        except TemplateSyntaxError:
            return text

    def send_mail(self, form):
        form_data = self.get_form_data(form)
        message = self.compile_message(form_data)
        context_dict = self.get_form_data_dict(form_data)

        import re 
        mail_to = re.compile('\s*[,;]+\s*').split(self.mail_to)
        for key, email in enumerate(mail_to):
            mail_to[key] = self.string_template_replace(email, context_dict)
        
        mail_from = self.mail_from or None
        if mail_from:
            mail_from = self.string_template_replace(mail_from, context_dict)
        
        if self.mail_subject:
            mail_subject = self.string_template_replace(self.mail_subject, context_dict)
        else:
            mail_subject = self.title
        
        import logging
        logging.debug('Mail: '+repr(mail_from)+' --> '+repr(mail_to));
        
        from django.core.mail import send_mail
        send_mail(mail_subject, message, mail_from or None, mail_to, fail_silently=False)

    @property
    def submit_flag_name(self):
        name = app_settings.get('FORM_DESIGNER_SUBMIT_FLAG_NAME') % self.name
        while self.formdefinitionfield_set.filter(name__exact=name).count() > 0:
            name += '_'
        return name

class FormLog(models.Model):
    created = models.DateTimeField(_('Created'), auto_now=True)
    form_definition = models.ForeignKey(FormDefinition, verbose_name=_('Form'))
    data = PickledObjectField(_('Data'), null=True, blank=True)

    class Meta:
        verbose_name = _('Form log')
        verbose_name_plural = _('Form logs')
        ordering = ['-created']

class FormDefinitionField(models.Model):

    form_definition = models.ForeignKey(FormDefinition)
    field_class = models.CharField(_('Field class'), choices=app_settings.get('FORM_DESIGNER_FIELD_CLASSES'), max_length=32)
    position = models.IntegerField(_('Position'), blank=True, null=True)

    name = models.SlugField(_('Name'), max_length=255)
    label = models.CharField(_('Label'), max_length=255, blank=True, null=True)
    required = models.BooleanField(_('Required'), default=True)
    include_result = models.BooleanField(_('Include in result'), help_text=('If this is disabled, the field value will not be included in logs and e-mails generated from form data.'), default=True)
    widget = models.CharField(_('Widget'), default='', choices=app_settings.get('FORM_DESIGNER_WIDGET_CLASSES'), max_length=255, blank=True, null=True)
    initial = models.CharField(_('Initial value'), max_length=255, blank=True, null=True)
    help_text = models.CharField(_('Help text'), max_length=255, blank=True, null=True)

    choice_values = models.TextField(_('Values'), help_text=_('One value per line'), blank=True, null=True)
    choice_labels = models.TextField(_('Labels'), help_text=_('One label per line'), blank=True, null=True)

    max_length = models.IntegerField(_('Max. length'), blank=True, null=True)
    min_length = models.IntegerField(_('Min. length'), blank=True, null=True)
    max_value = models.FloatField(_('Max. value'), blank=True, null=True)
    min_value = models.FloatField(_('Min. value'), blank=True, null=True)
    max_digits = models.IntegerField(_('Max. digits'), blank=True, null=True)
    decimal_places = models.IntegerField(_('Decimal places'), blank=True, null=True)

    regex = models.CharField(_('Regular Expression'), max_length=255, blank=True, null=True)

    choice_model_choices = app_settings.get('FORM_DESIGNER_CHOICE_MODEL_CHOICES')
    choice_model = ModelNameField(_('Data model'), max_length=255, blank=True, null=True, choices=choice_model_choices, help_text=('your_app.models.ModelName' if not choice_model_choices else None))
    choice_model_empty_label = models.CharField(_('Empty label'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')

    def save(self):
        if self.position == None:
            self.position = 0
        super(FormDefinitionField, self).save()

    def ____init__(self, field_class=None, name=None, required=None, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):
        super(FormDefinitionField, self).__init__(*args, **kwargs)
        self.name = name
        self.field_class = field_class
        self.required = required
        self.widget = widget
        self.label = label
        self.initial = initial
        self.help_text = help_text

    def get_form_field_init_args(self):
        args = {
            'required': self.required,
            'label': self.label if self.label else '',
            'initial': self.initial if self.initial else None,
            'help_text': self.help_text,
        }
        
        if self.field_class in ('forms.CharField', 'forms.EmailField', 'forms.RegexField'):
            args.update({
                'max_length': self.max_length,
                'min_length': self.min_length,
            })

        if self.field_class in ('forms.IntegerField', 'forms.DecimalField'):
            args.update({
                'max_value': int(self.max_value) if self.max_value != None else None,
                'min_value': int(self.min_value) if self.min_value != None else None,
            })

        if self.field_class == 'forms.DecimalField':
            args.update({
                'max_value': self.max_value,
                'min_value': self.min_value,
                'max_digits': self.max_digits,
                'decimal_places': self.decimal_places,
            })

        if self.field_class == 'forms.RegexField':
            if self.regex:
                args.update({
                    'regex': self.regex
                })

        if self.field_class in ('forms.ChoiceField', 'forms.MultipleChoiceField'):
            if self.choice_values:
                choices = []
                regex = re.compile('[\s]*\n[\s]*')
                values = regex.split(self.choice_values)
                labels = regex.split(self.choice_labels) if self.choice_labels else []
                for index, value in enumerate(values):
                    try:
                        label = labels[index]
                    except:
                        label = value
                    choices.append((value, label))
                args.update({
                    'choices': tuple(choices)
                })

        if self.field_class in ('forms.ModelChoiceField', 'forms.ModelMultipleChoiceField'):
            args.update({
                'queryset': ModelNameField.get_model_from_string(self.choice_model).objects.all()
            })
        
        if self.field_class == 'forms.ModelChoiceField':
            args.update({
                'empty_label': self.choice_model_empty_label
            })

        if self.widget:
            args.update({
                'widget': eval(self.widget)()
            })
        
        return args

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')
        ordering = ['position']

    def __unicode__(self):
        return self.label if self.label else self.name

if 'cms' in settings.INSTALLED_APPS:
    from cms.models import CMSPlugin

    class CMSFormDefinition(CMSPlugin):
        form_definition = models.ForeignKey(FormDefinition, verbose_name=_('Form'))

        def __unicode__(self):
            return self.form_definition.__unicode__()
