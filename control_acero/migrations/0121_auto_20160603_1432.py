# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0120_auto_20160602_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='cantidadReal',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
        migrations.AddField(
            model_name='salida',
            name='cantidadReal',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
    ]
