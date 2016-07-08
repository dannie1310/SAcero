# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0162_inventariofisico_estatusregistro'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisico',
            name='noEntradas',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventariofisico',
            name='noSalidas',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventariofisico',
            name='toneladaEntradas',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventariofisico',
            name='toneladaSalida',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventariofisico',
            name='totalExistencias',
            field=models.IntegerField(null=True),
        ),
    ]
