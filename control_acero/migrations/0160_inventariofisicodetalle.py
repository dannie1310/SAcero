# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0159_inventariofisico'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventarioFisicoDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pesoExistencia', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('pesoFisico', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('diferencia', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('tipoExistencia', models.IntegerField(default=0, choices=[(0, 'Existente'), (1, 'Inexistente')])),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('inventarioFisico', models.ForeignKey(to='control_acero.InventarioFisico', null=True)),
                ('material', models.ForeignKey(to='control_acero.Material', null=True)),
            ],
        ),
    ]
