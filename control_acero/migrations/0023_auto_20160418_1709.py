# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0022_auto_20160418_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elemento',
            old_name='alto',
            new_name='diametro',
        ),
        migrations.RenameField(
            model_name='elemento',
            old_name='ancho',
            new_name='longitudTotal',
        ),
        migrations.RenameField(
            model_name='elemento',
            old_name='longitud',
            new_name='numero',
        ),
        migrations.AddField(
            model_name='elemento',
            name='peso',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='despiece',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='elemento',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='estructura',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='funcion',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ingenieria',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='taller',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transporte',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
