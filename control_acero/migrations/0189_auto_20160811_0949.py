# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0188_remision_observacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioremisiondetalle',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'En Proceso'), (2, 'Si')]),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'En Proceso'), (2, 'Si')]),
        ),
        migrations.AlterField(
            model_name='remisiondetalle',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'En Proceso'), (2, 'Si')]),
        ),
        migrations.AlterField(
            model_name='salida',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'En Proceso'), (2, 'Si')]),
        ),
    ]
