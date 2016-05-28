# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0109_despiece_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='funcionAnterior',
            field=models.ForeignKey(related_name='funcionAnterior', to='control_acero.Funcion', null=True),
        ),
    ]
