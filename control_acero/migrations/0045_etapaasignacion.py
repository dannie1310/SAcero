# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0044_auto_20160501_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtapaAsignacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pesoSolicitado', models.IntegerField()),
                ('pesoRecibido', models.IntegerField()),
                ('tiempoEntrega', models.IntegerField()),
                ('cantidadAsignada', models.IntegerField()),
                ('estatusEtapa', models.IntegerField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('controlAsignacion', models.ForeignKey(to='control_acero.ControlAsignacion')),
                ('funcion', models.ForeignKey(to='control_acero.Funcion')),
                ('taller', models.ForeignKey(to='control_acero.Taller')),
                ('transporte', models.ForeignKey(to='control_acero.Transporte')),
            ],
        ),
    ]
