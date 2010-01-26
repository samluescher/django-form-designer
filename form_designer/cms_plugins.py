from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from form_designer.models import CMSFormDefinition
from django.utils.translation import ugettext as _
from views import process_form
from form_designer import app_settings

class FormDesignerPlugin(CMSPluginBase):
    model = CMSFormDefinition
    name = _("Form")
    admin_preview = False

    def render(self, context, instance, placeholder):
        if instance.form_definition.form_template_name:
            self.render_template = instance.form_definition.form_template_name
        else:
            self.render_template = app_settings.get('FORM_DESIGNER_DEFAULT_FORM_TEMPLATE')
        return process_form(context['request'], instance.form_definition, is_cms_plugin=True)

plugin_pool.register_plugin(FormDesignerPlugin)
