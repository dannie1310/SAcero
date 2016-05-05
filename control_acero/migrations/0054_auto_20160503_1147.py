# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0053_etapaasignacion_idetapapertenece'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroCinco',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroCuatro',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroDiez',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroDoce',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroNueve',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroOcho',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroOnce',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroSeis',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='numeroSiete',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='programasuministrodetalle',
            name='total',
            field=models.DecimalField(default=Decimal('0.0000'), max_digits=20, decimal_places=4),
        ),
    ]
