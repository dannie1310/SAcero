# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0200_salida_estatusapoyo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salida',
            name='estatusApoyo',
            field=models.IntegerField(default=0),
        ),
    ]
