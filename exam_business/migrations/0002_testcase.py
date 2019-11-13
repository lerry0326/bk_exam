# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64, verbose_name='\u7528\u6237\u540d')),
                ('phone', models.CharField(max_length=64, verbose_name='\u7535\u8bdd')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='\u6700\u540e\u767b\u5f55\u65f6\u95f4')),
                ('email', models.EmailField(max_length=254, verbose_name='\u90ae\u7bb1')),
            ],
        ),
    ]
