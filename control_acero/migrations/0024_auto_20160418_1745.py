# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0023_auto_20160418_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('identificacion', models.IntegerField()),
                ('ubicacion', models.CharField(max_length=100)),
                ('kilometros', models.FloatField(default=0)),
                ('estatusFrente', models.IntegerField(choices=[(0, 'Pendiente'), (1, 'Liberado')], default=0)),
                ('estatus', models.IntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='taller',
            name='responsable',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='elemento',
            name='numero',
            field=models.CharField(max_length=10),
        ),
    ]
