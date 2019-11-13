# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_business', '0002_testcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business', models.CharField(max_length=64, verbose_name='\u4e1a\u52a1')),
                ('cluster', models.CharField(max_length=64, verbose_name='\u96c6\u7fa4')),
                ('host', models.CharField(max_length=64, verbose_name='\u4e3b\u673a')),
            ],
            options={
                'db_table': 'exam_business_host info',
                'verbose_name': '\u4e3b\u673a\u4fe1\u606f',
            },
        ),
        migrations.AlterModelOptions(
            name='testcase',
            options={'verbose_name': '\u6d4b\u8bd5\u6848\u4f8b'},
        ),
        migrations.AlterModelTable(
            name='testcase',
            table='exam_business_test_case',
        ),
    ]
