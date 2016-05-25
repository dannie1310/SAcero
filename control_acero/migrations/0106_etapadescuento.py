# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0105_auto_20160524_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtapaDescuento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('cantidad', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('remision', models.IntegerField()),
                ('cantidadRemision', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('cantidadAsignada', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('cantidadRestante', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('estatusEtapa', models.IntegerField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('tipoRecepcion', models.IntegerField(default=1, choices=[(0, 'Parcial'), (1, 'Total')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('etapa', models.ForeignKey(to='control_acero.Etapa')),
            ],
        ),
    ]
