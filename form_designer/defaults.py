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
    ('html/form_definition/forms/as_p.html', _('as paragraphs')),
    ('html/form_definition/forms/as_table.html', _('as table')),
)

FORM_DESIGNER_DEFAULT_FORM_TEMPLATE = 'html/form_definition/forms/as_p.html'

