# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from conf.default import APP_ID, APP_TOKEN, BK_TOKEN, BK_USERNAME
from common.mymako import render_mako_context, render_json


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/index.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


# def test(request):
#     """测试接口"""
#     return render_json({'result': True, 'data': 'test api'})


def test(request):
    return render_json({'username': 'admin',
                       'phone': '18800000000',
                       'last_login': '2019-10-25 10:00:00',
                       'result': True,
                       'email': 'admin@qq.com'})


def get_app_info(request):
    client = get_client_by_request(request)
    resp = client.bk_paas.get_app_info(bk_app_code=APP_ID, bk_app_secret=APP_TOKEN, bk_username=BK_USERNAME)
    return render_json(resp['data'])


def get_userinfo(request):
    username = request.user
    print 1111111111, username
    if username == 'AnonymousUser':
        return render_json({'username': 'AnonymousUser', 'result': 'OK'})
    return render_json({'username': 'admin', 'result': 'OK'})
