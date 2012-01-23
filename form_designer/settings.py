import os.path

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import get_storage_class

STATIC_URL = os.path.join(getattr(settings, 'STATIC_URL', settings.MEDIA_URL), 'form_designer')

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

EXPORTER_CLASSES = getattr(settings, 'FORM_DESIGNER_WIDGET_CLASSES', (
    'form_designer.contrib.exporters.csv_exporter.CsvExporter',
    'form_designer.contrib.exporters.xls_exporter.XlsExporter',
))

FORM_TEMPLATES = getattr(settings, 'FORM_DESIGNER_FORM_TEMPLATES', (
    ('', _('Default')),
    ('html/formdefinition/forms/as_p.html', _('as paragraphs')),
    ('html/formdefinition/forms/as_table.html', _('as table')),
    ('html/formdefinition/forms/as_table_h.html', _('as table (horizontal)')),
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

CSV_EXPORT_ENCODING = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_ENCODING', 'utf-8')

CSV_EXPORT_NULL_VALUE = getattr(settings, 'FORM_DESIGNER_CSV_EXPORT_NULL_VALUE', '')

SUBMIT_FLAG_NAME = getattr(settings, 'FORM_DESIGNER_SUBMIT_FLAG_NAME', 'submit__%s')

FILE_STORAGE_CLASS = getattr(settings, 'FORM_DESIGNER_FILE_STORAGE_CLASS', get_storage_class())

FILE_STORAGE_DIR = 'form_uploads'

ALLOWED_FILE_TYPES = getattr(settings, 'FORM_DESIGNER_ALLOWED_FILE_TYPES', (
    'aac', 'ace', 'ai', 'aiff', 'avi', 'bmp', 'dir', 'doc', 'docx', 'dmg', 'eps', 'fla', 'flv', 
    'gif', 'gz', 'hqx', 'ico', 'indd', 'inx', 'jpg', 'jar', 'jpeg', 'md', 'mov', 
    'mp3', 'mp4', 'mpc', 'mkv', 'mpg', 'mpeg', 'ogg', 'odg', 'odf', 'odp', 'ods', 'odt', 'otf', 
    'pdf', 'png', 'pps', 'ppsx', 'ps', 'psd', 'rar', 'rm', 'rtf', 'sit', 'swf', 'tar', 'tga', 
    'tif', 'tiff', 'ttf', 'txt', 'wav', 'wma', 'wmv', 'xls', 'xlsx', 'xml', 'zip'
))

MAX_UPLOAD_SIZE = getattr(settings, 'MAX_UPLOAD_SIZE', 5242880) # 5M

VALUE_PICKLEFIELD = getattr(settings, 'FORM_DESIGNER_VALUE_PICKLEFIELD', False)
