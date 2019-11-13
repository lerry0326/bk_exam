# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    # (r'^test/$', 'test'),
    (r'^get_app_info/$', 'get_app_info'),
    (r'^api/test/$', 'get_userinfo')
)
