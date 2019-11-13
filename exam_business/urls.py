# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers as drf_routers
from .views import TaskViewSet, TestCaseViewSet, HostInfoViewSet


routers = drf_routers.DefaultRouter(trailing_slash=True)

routers.register(r'tasks', TaskViewSet, base_name='tasks')
routers.register(r'test', TestCaseViewSet)
routers.register(r'host', HostInfoViewSet)

urlpatterns = [
    url(r'api/', include(routers.urls))
]