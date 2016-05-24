# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0102_programasuministro_funcionhabilitado'),
    ]

    operations = [
        migrations.AddField(
            model_name='taller',
            name='funcion',
            field=models.ForeignKey(to='control_acero.Funcion', null=True),
        ),
    ]
