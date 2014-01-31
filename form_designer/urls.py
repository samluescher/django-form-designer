from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<object_name>[-\w]+)/$', 'form_designer.views.detail', name='form_designer_detail'),
    url(r'^h/(?P<public_hash>[-\w]+)/$', 'form_designer.views.detail_by_hash', name='form_designer_detail_by_hash'),
)
