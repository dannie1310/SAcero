# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0183_remove_inventariosalida_inventarioremisiondetalle'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescuentoSalida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pesoSalida', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('pesoRemision', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('resta', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('inventarioRemisionDetalle', models.ForeignKey(to='control_acero.InventarioRemisionDetalle', null=True)),
                ('inventarioSalida', models.ForeignKey(to='control_acero.InventarioSalida', null=True)),
            ],
        ),
    ]
