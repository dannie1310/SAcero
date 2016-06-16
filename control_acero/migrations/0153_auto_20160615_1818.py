# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0152_auto_20160615_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrada',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='inventarioremisiondetalle',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='inventariosalida',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='remisiondetalle',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='salida',
            name='cantidad',
        ),
    ]
