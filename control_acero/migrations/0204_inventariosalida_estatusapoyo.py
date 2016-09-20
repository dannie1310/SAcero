# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0203_entrada_armador'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariosalida',
            name='estatusApoyo',
            field=models.IntegerField(default=0),
        ),
    ]
