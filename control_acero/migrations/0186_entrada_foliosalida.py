# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0185_auto_20160808_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='folioSalida',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
