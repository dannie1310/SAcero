# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0140_inventariosalida'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradadetalle',
            name='calculado',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
    ]
