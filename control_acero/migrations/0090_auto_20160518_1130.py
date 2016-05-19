# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0089_auto_20160518_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='controlAsignacion',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='pesoRecibido',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='pesoSolicitado',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='piezasRecibidas',
        ),
        migrations.AddField(
            model_name='etapaasignacion',
            name='cantidad',
            field=models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3),
        ),
        migrations.AddField(
            model_name='etapaasignacion',
            name='peso',
            field=models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='etapaasignacion',
            name='cantidadAsignada',
            field=models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3),
        ),
    ]
