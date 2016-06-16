# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0154_auto_20160615_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='cantidadAsignada',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='cantidadReal',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='peso',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='entradadetalle',
            name='calculado',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='entradadetalle',
            name='longitud',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='entradadetalle',
            name='piezas',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='inventarioremisiondetalle',
            name='peso',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='cantidadAsignada',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='cantidadReal',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='peso',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='remision',
            name='pesoBruto',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='remision',
            name='pesoNeto',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='remision',
            name='pesoTara',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='remisiondetalle',
            name='peso',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidadAsignada',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidadReal',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='salida',
            name='peso',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
    ]
