# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0104_auto_20160524_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taller',
            name='proveedor',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
