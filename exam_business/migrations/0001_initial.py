# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u4efb\u52a1\u540d\u79f0')),
                ('status', models.SmallIntegerField(default=2, null=True, verbose_name='\u4efb\u52a1\u72b6\u6001', blank=True, choices=[(1, b'PENDING_APPLICATION'), (2, b'PENDING_APPROVAL'), (3, b'REJECTED'), (4, b'APPROVED')])),
                ('type', models.SmallIntegerField(default=1, null=True, verbose_name='\u4efb\u52a1\u7c7b\u578b', blank=True, choices=[(1, b'CREATE'), (2, b'UPDATE'), (3, b'DELETE')])),
            ],
            options={
                'db_table': 'exam_business_task',
                'verbose_name': '\u4efb\u52a1',
            },
        ),
    ]
