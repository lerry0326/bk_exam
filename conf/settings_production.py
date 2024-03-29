# -*- coding: utf-8 -*-
"""
用于正式环境的全局配置
"""
from settings import APP_ID


# ===============================================================================
# 数据库设置, 正式环境数据库设置
# ===============================================================================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
#         'NAME': APP_ID + '-o',                 # 数据库名 (默认与APP_ID相同)
#         'USER': 'root',                        # 你的数据库user
#         'PASSWORD': 'bk@321',                  # 你的数据库password
#         'HOST': '192.168.163.205',             # 数据库HOST
#         'PORT': '3306',                        # 默认3306
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
        'NAME': APP_ID,                 # 数据库名 (默认与APP_ID相同)
        'USER': 'examer',                        # 你的数据库user
        'PASSWORD': 'mypwd',                  # 你的数据库password
        'HOST': '192.168.165.187',             # 数据库HOST
        'PORT': '3306',                        # 默认3306
    },
}
