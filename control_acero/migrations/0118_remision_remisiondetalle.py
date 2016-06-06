# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0117_auto_20160602_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idOrden', models.IntegerField()),
                ('remision', models.IntegerField(null=True)),
                ('pesoTara', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('pesoBruto', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('pesoNeto', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('fechaRemision', models.DateField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente')),
                ('funcion', models.ForeignKey(to='control_acero.Funcion', null=True)),
                ('funcionHabilitado', models.ForeignKey(related_name='funcionHabilitado', to='control_acero.Funcion', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemisionDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('cantidad', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('longitud', models.IntegerField(null=True)),
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
