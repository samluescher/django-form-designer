from form_designer.models import FormDefinition
from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CMSFormDefinition(CMSPlugin):
    form_definition = models.ForeignKey(FormDefinition, verbose_name=_('form'))

    def __unicode__(self):
        return self.form_definition.__unicode__()
