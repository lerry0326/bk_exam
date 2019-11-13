# -*- coding: utf-8 -*-
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
import datetime
# 启动celery命令：
# 	python  manage.py  celery  worker  --settings=settings
# 	周期性任务还需要启动celery调度命令：
# 	python  manage.py  celerybeat --settings=settings


@task
def execute_task():
    pass

# 每分钟执行一次
@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week='*'))
def send_msg():
    pass


def test_async_task(request):
    execute_task.delay()
    return


def test_reserve_time(request):
    # 10秒后执行
    execute_task.apply_async(eta=datetime.datetime.now() + datetime.timedelta(seconds=10))
    return