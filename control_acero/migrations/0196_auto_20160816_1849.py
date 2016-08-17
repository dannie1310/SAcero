# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0195_salida_estatusreposicion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcion',
            name='proveedor',
            field=models.CharField(max_length=20),
        ),
    ]
