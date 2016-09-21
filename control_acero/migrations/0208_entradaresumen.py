# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0207_entrada'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntradaResumen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pesoRemision', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('pesoReal', models.DecimalField(default=Decimal('0.00'), null=True, max_digits=20, decimal_places=2)),
                ('tipoRecepcion', models.IntegerField(default=1, choices=[(0, 'Completo'), (1, 'Faltante'), (2, 'Sobrante')])),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('entrada', models.ForeignKey(to='control_acero.Entrada', null=True)),
                ('material', models.ForeignKey(to='control_acero.Material', null=True)),
            ],
        ),
    ]
