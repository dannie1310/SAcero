# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0209_entradadetalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='remision',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventariosalida',
            name='remision',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='remision',
            name='remision',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='salida',
            name='remision',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
