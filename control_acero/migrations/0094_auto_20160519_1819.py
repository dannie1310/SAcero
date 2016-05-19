# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0093_auto_20160519_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtapaAsignacionDespieceDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('despiecePeso', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('despiece', models.ForeignKey(to='control_acero.Despiece')),
            ],
        ),
        migrations.AddField(
            model_name='etapaasignaciondespiece',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='etapaasignaciondespiece',
            name='EtapaAsignacionDespieceDetalle',
            field=models.ManyToManyField(to='control_acero.EtapaAsignacionDespieceDetalle', blank=True),
        ),
    ]
