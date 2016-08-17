# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0192_remision_pesototal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcion',
            name='tonelajeMaximo',
        ),
        migrations.AddField(
            model_name='funcion',
            name='porcentajeMaximo',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
    ]
