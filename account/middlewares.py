# -*- coding: utf-8 -*-
"""Login middleware."""

from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import get_token as get_csrf_token
from django.conf import settings

from account.accounts import Account


class LoginMiddleware(object):
    """Login middleware."""

    def process_view(self, request, view, args, kwargs):
        """process_view."""
        # 模拟登录账号
        username = 'admin'
        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            user = user_model.objects.get(username=username)
        else:
            user = user_model.objects.create(username=username, chname=username, is_staff=False, is_superuser=False,
                                             is_in_app=True)
        request.user = user
        # 存入csrf值到cookies
        request.META.update({
            "CSRF_COOKIE_USED": True,
        })
        return None
        if getattr(view, 'login_exempt', False):
            return None

        # 对[公众号]weixin 路径不需要蓝鲸登录
        use_weixin = getattr(settings, "USE_WEIXIN", None)
        weixin_path_prefix = getattr(settings, "WEIXIN_SITE_URL", None)
        weixin_app_external_host = getattr(settings, "WEIXIN_APP_EXTERNAL_HOST", None)
        if (use_weixin and weixin_path_prefix and weixin_app_external_host and
                request.path.startswith(weixin_path_prefix) and request.get_host() == weixin_app_external_host):
            return None

        # 对于微信小程序的路径不需要蓝鲸登录
        use_miniweixin = getattr(settings, "USE_MINIWEIXIN", None)
        miniweixin_path_prefix = getattr(settings, "MINIWEIXIN_SITE_URL", None)
        miniweixin_app_external_host = getattr(settings, "MINIWEIXIN_APP_EXTERNAL_HOST", None)
        if (use_miniweixin and miniweixin_path_prefix and miniweixin_app_external_host and
                request.path.startswith(miniweixin_path_prefix) and request.get_host() == miniweixin_app_external_host):
            return None

        user = authenticate(request=request)
        if user:
            request.user = user
            get_csrf_token(request)
            return None

        account = Account()
        return account.redirect_login(request)


class DisableCSRFCheck(object):
    """
    本地开发，去掉django rest framework强制的csrf检查
    """

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return None
