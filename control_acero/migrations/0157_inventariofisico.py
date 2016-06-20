# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0156_frente_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventarioFisico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidadPiezas', models.IntegerField()),
                ('longitud', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('atado', models.IntegerField(null=True)),
                ('nomenclatura', models.CharField(max_length=10, null=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('elemento', models.ForeignKey(to='control_acero.Elemento', null=True)),
                ('material', models.ForeignKey(to='control_acero.Material', null=True)),
            ],
        ),
    ]
