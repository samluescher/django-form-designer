from django.utils.translation import ugettext_lazy as _

FORM_DESIGNER_FIELD_CLASSES = (
    ('forms.CharField', _('Text')),
    ('forms.EmailField', _('E-mail address')),
    ('forms.URLField', _('Web address')),
    ('forms.IntegerField', _('Number')),
    ('forms.DecimalField', _('Decimal number')),
    ('forms.BooleanField', _('Yes/No')),
    ('forms.DateField', _('Date')),
    ('forms.DateTimeField', _('Date & time')),
    ('forms.TimeField', _('Time')),
    ('forms.ChoiceField', _('Choice')),
    ('forms.MultipleChoiceField', _('Multiple Choice')),
    ('forms.RegexField', _('Regex')),
)

FORM_DESIGNER_WIDGET_CLASSES = (
    ('', _('Default')),
    ('widgets.Textarea', _('Text area')),
    ('widgets.PasswordInput', _('Password input')),
    ('widgets.HiddenInput', _('Hidden input')),
)

FORM_DESIGNER_FORM_TEMPLATES = (
    ('', _('Default')),
    ('html/formdefinition/forms/as_p.html', _('as paragraphs')),
    ('html/formdefinition/forms/as_table.html', _('as table')),
)

FORM_DESIGNER_DEFAULT_FORM_TEMPLATE = 'html/formdefinition/forms/as_p.html'

# semicolon is Microsoft Excel default
FORM_DESIGNER_CSV_EXPORT_DELIMITER = ';'

# include log timestamp in export
FORM_DESIGNER_CSV_EXPORT_INCLUDE_CREATED = True

# include field labels/names in first row if exporting logs for one form only
FORM_DESIGNER_CSV_EXPORT_INCLUDE_HEADER = True

# include form title if exporting logs for more than one form
FORM_DESIGNER_CSV_EXPORT_INCLUDE_FORM = True

FORM_DESIGNER_CSV_EXPORT_FILENAME = 'export.csv'

