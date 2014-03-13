# coding=utf-8
try:
    from django.conf.urls import patterns, url
except ImportError: # for Django < 1.4
    from django.conf.urls.defaults import patterns, url  # NOQA

urlpatterns = patterns('',
    url(r'^(?P<object_name>[-\w]+)/$', 'form_designer.views.detail', name='form_designer_detail'),
    url(r'^h/(?P<public_hash>[-\w]+)/$', 'form_designer.views.detail_by_hash', name='form_designer_detail_by_hash'),
)
