# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0158_auto_20160623_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventarioFisico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numFolio', models.IntegerField(null=True)),
                ('folio', models.CharField(max_length=20, null=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('tallerAsignado', models.ForeignKey(related_name='tallerAsignadoInventario', to='control_acero.Taller', null=True)),
            ],
        ),
    ]
