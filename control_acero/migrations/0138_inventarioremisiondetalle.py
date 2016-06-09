# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0137_taller_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventarioRemisionDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('cantidad', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('longitud', models.IntegerField(null=True)),
                ('numFolio', models.IntegerField(null=True)),
                ('folio', models.CharField(max_length=20, null=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('apoyo', models.ForeignKey(to='control_acero.Apoyo')),
                ('elemento', models.ForeignKey(to='control_acero.Elemento')),
                ('material', models.ForeignKey(to='control_acero.Material', null=True)),
                ('remision', models.ForeignKey(to='control_acero.Remision', null=True)),
            ],
        ),
    ]
