# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0160_inventariofisicodetalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioremisiondetalle',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'Si')]),
        ),
        migrations.AddField(
            model_name='inventarioremisiondetalle',
            name='folioInventario',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventariosalida',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'Si')]),
        ),
        migrations.AddField(
            model_name='inventariosalida',
            name='folioInventario',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='remisiondetalle',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'Si')]),
        ),
        migrations.AddField(
            model_name='remisiondetalle',
            name='folioInventario',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='estatusInventario',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'Si')]),
        ),
        migrations.AddField(
            model_name='salida',
            name='folioInventario',
            field=models.IntegerField(null=True),
        ),
    ]
