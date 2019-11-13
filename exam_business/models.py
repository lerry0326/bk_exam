# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Task(models.Model):
    TASK_STATUS_CHOICES = (
        (1, 'PENDING_APPLICATION'),
        (2, 'PENDING_APPROVAL'),
        (3, 'REJECTED'),
        (4, 'APPROVED')
    )
    TASK_TYPE_CHOICES = (
        (1, 'CREATE'),
        (2, 'UPDATE'),
        (3, 'DELETE')
    )
    name = models.CharField(max_length=64, verbose_name=u'任务名称')
    status = models.SmallIntegerField(choices=TASK_STATUS_CHOICES,
                                      default=2,
                                      blank=True,
                                      null=True,
                                      verbose_name=u'任务状态')
    type = models.SmallIntegerField(choices=TASK_TYPE_CHOICES,
                                    default=1,
                                    blank=True,
                                    null=True,
                                    verbose_name=u'任务类型')

    class Meta:
        db_table = 'exam_business_task'
        verbose_name = u'任务'

    def __str__(self):
        return self.name


class TestCase(models.Model):
    username = models.CharField(max_length=64, verbose_name=u'用户名')
    phone = models.CharField(max_length=64, verbose_name=u'电话')
    last_login = models.DateTimeField(auto_now_add=True, verbose_name=u'最后登录时间')
    email = models.EmailField(verbose_name=u'邮箱')

    class Meta:
        db_table = 'exam_business_test_case'
        verbose_name = u'测试案例'

    def __str__(self):
        return self.username


class HostInfo(models.Model):
    business = models.CharField(max_length=64, verbose_name=u'业务')
    cluster = models.CharField(max_length=64, verbose_name=u'集群')
    host = models.CharField(max_length=64, verbose_name=u'主机')

    class Meta:
        db_table = 'exam_business_host_info'
        verbose_name = u'主机信息'
