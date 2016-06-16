# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0151_auto_20160615_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='cantidadAsignada',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='cantidadReal',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='peso',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entradadetalle',
            name='calculado',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entradadetalle',
            name='longitud',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entradadetalle',
            name='piezas',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='cantidadAsignada',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='cantidadReal',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='peso',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidadAsignada',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidadReal',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='salida',
            name='peso',
            field=models.IntegerField(null=True),
        ),
    ]
