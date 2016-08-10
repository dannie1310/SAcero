# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0184_descuentosalida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descuentosalida',
            name='inventarioSalida',
        ),
        migrations.AddField(
            model_name='descuentosalida',
            name='estatusSalida',
            field=models.IntegerField(default=0, choices=[(0, 'Pendiente'), (1, 'Guardado')]),
        ),
        migrations.AddField(
            model_name='descuentosalida',
            name='salida',
            field=models.ForeignKey(to='control_acero.Salida', null=True),
        ),
    ]
