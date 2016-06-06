# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0118_remision_remisiondetalle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=3)),
                ('cantidad', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=3)),
                ('tiempoEntrega', models.IntegerField(null=True)),
                ('cantidadAsignada', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=3)),
                ('idEtapaPertenece', models.IntegerField(null=True)),
                ('idOrdenTrabajo', models.IntegerField(null=True)),
                ('estatusEtapa', models.IntegerField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('tipoEstatus', models.IntegerField(default=1, choices=[(1, 'En proceso'), (2, 'Recepcionado'), (3, 'Enviado'), (4, 'Rechazado')])),
                ('tipoRecepcion', models.IntegerField(default=1, choices=[(0, 'Parcial'), (1, 'Total')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('apoyo', models.ForeignKey(to='control_acero.Apoyo', null=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente', null=True)),
                ('funcion', models.ForeignKey(to='control_acero.Funcion', null=True)),
                ('material', models.ForeignKey(to='control_acero.Material', null=True)),
                ('taller', models.ForeignKey(to='control_acero.Taller', null=True)),
                ('transporte', models.ForeignKey(to='control_acero.Transporte', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Folio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modulo', models.IntegerField()),
                ('descripcion', models.CharField(max_length=10)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Salida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=3)),
                ('cantidad', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=3)),
                ('tiempoEntrega', models.IntegerField(null=True)),
                ('cantidadAsignada', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=3)),
                ('idEtapaPertenece', models.IntegerField(null=True)),
                ('idOrdenTrabajo', models.IntegerField(null=True)),
                ('estatusEtapa', models.IntegerField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('tipoEstatus', models.IntegerField(default=1, choices=[(1, 'En proceso'), (2, 'Recepcionado'), (3, 'Enviado'), (4, 'Rechazado')])),
                ('tipoRecepcion', models.IntegerField(default=1, choices=[(0, 'Parcial'), (1, 'Total')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('apoyo', models.ForeignKey(to='control_acero.Apoyo', null=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente', null=True)),
                ('funcion', models.ForeignKey(to='control_acero.Funcion', null=True)),
                ('material', models.ForeignKey(to='control_acero.Material', null=True)),
                ('taller', models.ForeignKey(to='control_acero.Taller', null=True)),
                ('transporte', models.ForeignKey(to='control_acero.Transporte', null=True)),
            ],
        ),
    ]
