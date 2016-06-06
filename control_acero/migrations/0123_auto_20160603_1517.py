# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0122_auto_20160603_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='estatusEtapa',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='salida',
            name='estatusEtapa',
            field=models.IntegerField(default=1),
        ),
    ]
