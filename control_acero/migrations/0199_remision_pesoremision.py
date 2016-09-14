# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0198_auto_20160824_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='remision',
            name='pesoRemision',
            field=models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2),
        ),
    ]
