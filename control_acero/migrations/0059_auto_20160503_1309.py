# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0058_auto_20160503_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapaasignacion',
            name='cantidadAsignada',
            field=models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='etapaasignacion',
            name='pesoRecibido',
            field=models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='etapaasignacion',
            name='pesoSolicitado',
            field=models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4),
        ),
    ]
