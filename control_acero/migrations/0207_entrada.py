# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0206_auto_20160921_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('folioSalida', models.CharField(max_length=20, null=True)),
                ('remision', models.CharField(max_length=20, null=True)),
                ('armador', models.CharField(max_length=100, null=True)),
                ('numFolio', models.IntegerField(null=True)),
                ('folio', models.CharField(max_length=20, null=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('apoyo', models.ForeignKey(to='control_acero.Apoyo', null=True)),
                ('elemento', models.ForeignKey(to='control_acero.Elemento', null=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente', null=True)),
                ('funcion', models.ForeignKey(to='control_acero.Funcion', null=True)),
                ('taller', models.ForeignKey(to='control_acero.Taller', null=True)),
            ],
        ),
    ]
