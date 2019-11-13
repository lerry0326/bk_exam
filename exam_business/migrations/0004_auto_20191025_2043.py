# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_business', '0003_auto_20191025_2002'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='hostinfo',
            table='exam_business_host_info',
        ),
    ]
