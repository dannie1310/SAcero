# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0054_auto_20160503_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='peso',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
    ]
