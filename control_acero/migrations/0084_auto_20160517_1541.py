# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0083_programasuministro_remision'),
    ]

    operations = [
        migrations.AddField(
            model_name='programasuministro',
            name='pesoBruto',
            field=models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3),
        ),
        migrations.AddField(
            model_name='programasuministro',
            name='pesoTara',
            field=models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3),
        ),
    ]
