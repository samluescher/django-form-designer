from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from form_designer.models import CMSFormDefinition
from django.utils.translation import ugettext as _
from views import process_form

class CMSFormDesignerPlugin(CMSPluginBase):
    model = CMSFormDefinition
    name = _("Form")
    render_template = 'html/form_definition/form_as_p.html'
    admin_preview = False

    def render(self, context, instance, placeholder):
        return process_form(context['request'], instance.form_definition)

plugin_pool.register_plugin(CMSFormDesignerPlugin)
