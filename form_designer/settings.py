from django.conf import settings
from django.utils.translation import ugettext_lazy as _

MEDIA_URL = getattr(settings, 'FORM_DESIGNER_MEDIA_URL', '%sform_designer/' % settings.MEDIA_URL)

FIELD_CLASSES = getattr(settings, 'FORM_DESIGNER_FIELD_CLASSES', (
    ('django.forms.CharField', _('Text')),
    ('django.forms.EmailField', _('E-mail address')),
    ('django.forms.URLField', _('Web address')),
    ('django.forms.IntegerField', _('Number')),
    ('django.forms.DecimalField', _('Decimal number')),
    ('django.forms.BooleanField', _('Yes/No')),
    ('django.forms.DateField', _('Date')),
    ('django.forms.DateTimeField', _('Date & time')),
    ('django.forms.TimeField', _('Time')),
    ('django.forms.ChoiceField', _('Choice')),
    ('django.forms.MultipleChoiceField', _('Multiple Choice')),
    ('django.forms.ModelChoiceField', _('Model Choice')),
    ('django.forms.ModelMultipleChoiceField', _('Model Multiple Choice')),
    ('django.forms.RegexField', _('Regex')),
    ('django.forms.FileField', _('File')),
    # ('captcha.fields.CaptchaField', _('Captcha')),
))

WIDGET_CLASSES = getattr(settings, 'FORM_DESIGNER_WIDGET_CLASSES', (
    ('', _('Default')),
    ('django.forms.widgets.Textarea', _('Text area')),
    ('django.forms.widgets.PasswordInput', _('Password input')),
    ('django.forms.widgets.HiddenInput', _('Hidden input')),
    ('django.forms.widgets.RadioSelect', _('Radio button')),
))

FORM_TEMPLATES = getattr(settings, 'FORM_DESIGNER_FORM_TEMPLATES', (
    ('', _('Default')),
    ('html/formdefinition/forms/as_p.html', _('as paragraphs')),
    ('html/formdefinition/forms/as_table.html', _('as table')),
    ('html/formdefinition/forms/as_ul.html', _('as unordered list')),
    ('html/formdefinition/forms/custom.html', _('custom implementation')),
))

# Sequence of two-tuples like (('your_app.models.ModelName', 'My Model'), ...) for limiting the models available to ModelChoiceField and ModelMultipleChoiceField.
# If None, any model can be chosen by entering it as a string
CHOICE_MODEL_CHOICES = getattr(settings, 'FORM_DESIGNER_CHOICE_MODEL_CHOICES', None)

DEFAULT_FORM_TEMPLATE = getattr(settings, 'FORM_DESIGNER_DEFAULT_FORM_TEMPLATE', 'html/formdefinition/forms/as_p.html')

# semicolon is Microsoft Excel default
CSV_EXPORT_DELIMITER = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_DELIMITER', ';')

# include log timestamp in export
CSV_EXPORT_INCLUDE_CREATED = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_INCLUDE_CREATED', True)

CSV_EXPORT_INCLUDE_PK = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_INCLUDE_PK', True)

# include field labels/names in first row if exporting logs for one form only
CSV_EXPORT_INCLUDE_HEADER = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_INCLUDE_HEADER', True)

# include form title if exporting logs for more than one form
CSV_EXPORT_INCLUDE_FORM = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_INCLUDE_FORM', True)

CSV_EXPORT_FILENAME = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_FILENAME', 'export.csv')

CSV_EXPORT_ENCODING = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_ENCODING', 'utf-8')

SUBMIT_FLAG_NAME = getattr(settings, 'FORM_DESIGNER_SUBMIT_FLAG_NAME', 'submit__%s')
