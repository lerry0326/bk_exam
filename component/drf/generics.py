# -*- coding: utf-8 -*-

import traceback
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.compat import set_rollback
from rest_framework.response import Response
from rest_framework.exceptions import (AuthenticationFailed, MethodNotAllowed, NotAuthenticated,
                                       PermissionDenied as RestPermissionDenied,
                                       ValidationError)
from django.http import Http404
from component.constants import ResponseCodeStatus
from common.log import logger


def exception_handler(exc, content):
    data = {
        'result': False,
        'data': None
    }
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        data = {
            'result': False,
            'code': ResponseCodeStatus.UNAUTHORIZED,
            'detail': u'用户未登录或登录态失效，请使用登录链接重新登录',
            'login_url': ''
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, PermissionDenied) or isinstance(exc, RestPermissionDenied):
        message = exc.detail if hasattr(exc, 'detail') else u'该用户没有该权限功能'
        data = {
            'result': False,
            'code': ResponseCodeStatus.PERMISSION_DENIED,
            'message': message
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    else:
        if isinstance(exc, ValidationError):

            if isinstance(exc.detail, list):
                message = '; '.join([u'{}:{}'.format(k, v) for k, v in enumerate(exc.detail)])
            elif isinstance(exc.detail, dict):
                message = '; '.join([u'{}:{}'.format(k, v) for k, v in exc.detail.iteritems()])
            else:
                message = exc.detail

            data.update({
                'code': ResponseCodeStatus.VALIDATE_ERROR,
                'message': message
            })

        elif isinstance(exc, MethodNotAllowed):
            data.update({
                'code': ResponseCodeStatus.METHOD_NOT_ALLOWED,
                'message': exc.detail,
            })

        elif isinstance(exc, Http404):
            # 更改返回的状态为为自定义错误类型的状态码
            data.update({
                'code': ResponseCodeStatus.OBJECT_NOT_EXIST,
                'message': exc.message,
            })
        else:
            # 调试模式
            logger.error(traceback.format_exc())
            print traceback.format_exc()
            # if settings.RUN_MODE != 'PRODUCT':
            #     raise exc
            # 正式环境，屏蔽500
            data.update({
                'code': ResponseCodeStatus.SERVER_500_ERROR,
                'message': exc.message,
            })

        set_rollback()
        return Response(data, status=status.HTTP_200_OK)


def validate_fields(data, *fields):
    """校验必填参数"""
    validations = []
    for field in fields:
        if field not in data:
            validations.append(u'%s该字段是必填项' % field)
    if validations:
        raise ValidationError(validations)
