# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0205_bitacora_justificacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrada',
            name='apoyo',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='elemento',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='frente',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='funcion',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='material',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='taller',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='tallerAsignado',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='transporte',
        ),
        migrations.RemoveField(
            model_name='entradadetalle',
            name='entrada',
        ),
        migrations.DeleteModel(
            name='Entrada',
        ),
        migrations.DeleteModel(
            name='EntradaDetalle',
        ),
    ]
