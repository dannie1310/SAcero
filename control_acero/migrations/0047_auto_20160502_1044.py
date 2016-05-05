# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0046_auto_20160502_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlasignacion',
            name='tiempoEntrega',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='etapaasignacion',
            name='cantidadAsignada',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='etapaasignacion',
            name='tiempoEntrega',
            field=models.IntegerField(null=True),
        ),
    ]
