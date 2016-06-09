# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0139_inventarioremisiondetalle_estatustotalizado'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventarioSalida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('cantidad', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('tiempoEntrega', models.IntegerField(null=True)),
                ('cantidadReal', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('cantidadAsignada', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('idEtapaPertenece', models.IntegerField(null=True)),
                ('idOrdenTrabajo', models.IntegerField(null=True)),
                ('remision', models.IntegerField(null=True)),
                ('estatusEtapa', models.IntegerField(default=1)),
                ('numFolio', models.IntegerField(null=True)),
                ('folio', models.CharField(max_length=20, null=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('estatusTotalizado', models.IntegerField(default=1)),
                ('tipoEstatus', models.IntegerField(default=1, choices=[(1, 'En proceso'), (2, 'Recepcionado'), (3, 'Enviado'), (4, 'Rechazado')])),
                ('tipoRecepcion', models.IntegerField(default=1, choices=[(0, 'Parcial'), (1, 'Total')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('apoyo', models.ForeignKey(to='control_acero.Apoyo', null=True)),
                ('elemento', models.ForeignKey(to='control_acero.Elemento', null=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente', null=True)),
                ('funcion', models.ForeignKey(to='control_acero.Funcion', null=True)),
                ('material', models.ForeignKey(to='control_acero.Material', null=True)),
                ('taller', models.ForeignKey(to='control_acero.Taller', null=True)),
                ('tallerAsignado', models.ForeignKey(related_name='tallerAsignadoSalidaInventario', to='control_acero.Taller', null=True)),
                ('transporte', models.ForeignKey(to='control_acero.Transporte', null=True)),
            ],
        ),
    ]
