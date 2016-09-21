# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0208_entradaresumen'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntradaDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomenclatura', models.CharField(max_length=20, null=True)),
                ('longitud', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('piezas', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('calculado', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('entradaResumen', models.ForeignKey(to='control_acero.EntradaResumen', null=True)),
            ],
        ),
    ]
