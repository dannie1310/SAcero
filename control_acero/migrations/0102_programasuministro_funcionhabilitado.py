# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0101_auto_20160521_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='programasuministro',
            name='funcionHabilitado',
            field=models.ForeignKey(related_name='funcionHabilitado', to='control_acero.Funcion', null=True),
        ),
    ]
