# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 18:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0010_auto_20160418_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despiece',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 95000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='elemento',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 95000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='estructura',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 95000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='funcion',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 100000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ingenieria',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 95000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='material',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 95000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='taller',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 100000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transporte',
            name='fechaRegistro',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 18, 12, 39, 95000, tzinfo=utc)),
        ),
    ]
