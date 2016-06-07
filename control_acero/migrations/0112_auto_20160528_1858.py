# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0110_etapa_funcionanterior'),
    ]

    operations = [
        migrations.CreateModel(
            name='inventarioFisico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('despiece', models.IntegerField()),
                ('elemento', models.IntegerField()),
                ('apoyo', models.IntegerField()),
                ('cantidadFisica', models.IntegerField()),
                ('longitudFisica', models.IntegerField()),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('frente', models.ForeignKey(to='control_acero.Frente')),
                ('proveedor', models.ForeignKey(to='control_acero.Funcion')),
            ],
        ),
        
    ]
