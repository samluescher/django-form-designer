from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from form_designer.models import CMSFormDefinition
from form_designer.views import process_form
from form_designer import settings

class FormDesignerPlugin(CMSPluginBase):
    model = CMSFormDefinition
    name = _("Form")
    admin_preview = False

    def render(self, context, instance, placeholder):
        if instance.form_definition.form_template_name:
            self.render_template = instance.form_definition.form_template_name
        else:
            self.render_template = settings.DEFAULT_FORM_TEMPLATE
        return process_form(context['request'], instance.form_definition, context, is_cms_plugin=True)

plugin_pool.register_plugin(FormDesignerPlugin)
