# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0119_entrada_folio_salida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='cantidad',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='cantidadAsignada',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='entrada',
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
            name='cantidad',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='remisiondetalle',
            name='peso',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidad',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='salida',
            name='cantidadAsignada',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='salida',
            name='peso',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
    ]
