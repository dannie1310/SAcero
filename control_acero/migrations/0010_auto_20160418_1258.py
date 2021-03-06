# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 17:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0009_auto_20160418_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(1, 'Suministrador'), (2, 'Habilitador'), (3, 'Armador'), (3, 'Colocador')], default=1)),
                ('proveedor', models.CharField(default=0, max_length=20)),
                ('tonelajeMaximo', models.FloatField(default=0)),
                ('estatus', models.IntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('fechaRegistro', models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 743000, tzinfo=utc))),
            ],
        ),
        migrations.DeleteModel(
            name='Funciones',
        ),
        migrations.AlterField(
            model_name='despiece',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 743000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='elemento',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 743000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='estructura',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 743000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ingenieria',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 743000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='material',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 738000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='taller',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 743000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transporte',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 17, 58, 33, 743000, tzinfo=utc)),
        ),
    ]
