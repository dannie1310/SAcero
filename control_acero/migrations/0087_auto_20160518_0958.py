# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0086_programasuministro_funcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='cantidad',
            field=models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='peso',
            field=models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3),
        ),
    ]
