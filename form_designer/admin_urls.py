from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
    url(r'^formlog/export_csv/$', 'form_designer.admin_views.export_csv', name='form_designer_export_csv'),
    
)
