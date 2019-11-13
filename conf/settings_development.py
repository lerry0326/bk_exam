# -*- coding: utf-8 -*-
"""
用于本地开发环境的全局配置
"""
from settings import APP_ID, MIDDLEWARE_CLASSES
from settings import MIDDLEWARE_CLASSES


# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'demo',                        # 数据库名 (默认与APP_ID相同)
    },
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
        'NAME': 'bk_exam',                        # 数据库名 (默认与APP_ID相同)
        'USER': 'root',                        # 你的数据库user
        'PASSWORD': 'mysql',                        # 你的数据库password
        'HOST': 'localhost',                   # 开发的时候，使用localhost
        'PORT': '3306',                        # 默认3306
    },
}

# 将celery异步任务更改为同步
CELERY_ALWAYS_EAGER = True

MIDDLEWARE_CLASSES += (
    'corsheaders.middleware.CorsMiddleware',
    'account.middlewares.DisableCSRFCheck'
)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True