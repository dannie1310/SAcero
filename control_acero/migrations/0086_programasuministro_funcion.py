# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0085_programasuministro_pesoneto'),
    ]

    operations = [
        migrations.AddField(
            model_name='programasuministro',
            name='funcion',
            field=models.ForeignKey(to='control_acero.Funcion', null=True),
        ),
    ]
