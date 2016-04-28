# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0030_auto_20160427_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elemento',
            old_name='numero',
            new_name='tipo',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='despiece',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='diametro',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='longitudTotal',
        ),
        migrations.AddField(
            model_name='elemento',
            name='fechaActualizacion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='elemento',
            name='material',
            field=models.ManyToManyField(to='control_acero.Material', blank=True),
        ),
    ]
