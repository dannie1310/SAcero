# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0204_inventariosalida_estatusapoyo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitacora',
            name='justificacion',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
