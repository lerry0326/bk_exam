# -*- coding: utf-8 -*-
"""
权限校验类

class XxxPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

"""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    是否为APP管理员
    """

    def has_permission(self, request, view):
        return request.user.is_superuser