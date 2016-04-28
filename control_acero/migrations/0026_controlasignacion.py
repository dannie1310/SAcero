# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0025_auto_20160420_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlAsignacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('tiempoEntrega', models.IntegerField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente')),
                ('funcion', models.ForeignKey(to='control_acero.Funcion')),
            ],
        ),
    ]
