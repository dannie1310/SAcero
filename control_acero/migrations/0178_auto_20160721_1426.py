# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0177_auto_20160721_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventarioFisicoDetalleCompleto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('piezas', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('longitud', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('estatusTipoV', models.IntegerField(default=0, choices=[(0, 'No'), (1, 'No Habilitada'), (2, 'Proceso'), (3, 'Habilitada')])),
                ('referencia', models.CharField(max_length=25, null=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='inventariofisicodetalle',
            name='estatusTipoV',
        ),
        migrations.RemoveField(
            model_name='inventariofisicodetalle',
            name='referencia',
        ),
        migrations.AddField(
            model_name='inventariofisicodetallecompleto',
            name='InventarioFisicoDetalle',
            field=models.ForeignKey(to='control_acero.InventarioFisicoDetalle', null=True),
        ),
        migrations.AddField(
            model_name='inventariofisicodetallecompleto',
            name='material',
            field=models.ForeignKey(to='control_acero.Material', null=True),
        ),
    ]
