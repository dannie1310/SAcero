# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0103_taller_funcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taller',
            name='proveedor',
            field=models.CharField(default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='taller',
            name='responsable',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
