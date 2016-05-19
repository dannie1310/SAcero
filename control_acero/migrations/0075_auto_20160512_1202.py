# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0074_auto_20160512_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='diametro',
            field=models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4),
        ),
    ]
