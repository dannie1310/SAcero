# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0036_material_numero'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramaSuministro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idOrden', models.IntegerField()),
                ('fechaInicial', models.DateTimeField()),
                ('fechaFinal', models.DateTimeField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramaSuministroDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idProgramaSuministro', models.IntegerField()),
                ('numeroCuatro', models.CharField(max_length=20)),
                ('numeroCinco', models.CharField(max_length=20)),
                ('numeroSeis', models.CharField(max_length=20)),
                ('numeroSiete', models.CharField(max_length=20)),
                ('numeroOcho', models.CharField(max_length=20)),
                ('numeroNueve', models.CharField(max_length=20)),
                ('numeroDiez', models.CharField(max_length=20)),
                ('numeroOnce', models.CharField(max_length=20)),
                ('numeroDoce', models.CharField(max_length=20)),
                ('total', models.CharField(max_length=20)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('apoyo', models.ForeignKey(to='control_acero.Apoyo')),
                ('elemento', models.ForeignKey(to='control_acero.Elemento')),
            ],
        ),
    ]
