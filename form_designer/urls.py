from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<object_name>[-\w]+)/$', 'form_designer.views.detail', name='form_designer_detail'),
)
