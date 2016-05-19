# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0092_etapaasignacion_programasuministro'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtapaAsignacionDespiece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('despieceTotal', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('pesoRecibido', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('pesoRestante', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('elemento', models.ForeignKey(to='control_acero.Elemento')),
                ('material', models.ForeignKey(to='control_acero.Material')),
            ],
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='despiece',
        ),
        migrations.AddField(
            model_name='etapaasignacion',
            name='EtapaAsignacionDespiece',
            field=models.ManyToManyField(to='control_acero.EtapaAsignacionDespiece', blank=True),
        ),
    ]
