# coding: utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns('constructor_forms.views',
    url(r'(?P<slug>.*)/sent/$', 'form_sent', name='FormSent'),
    url(r'(?P<slug>.*)/$', 'form_detail', name='FormDetail'),
)
