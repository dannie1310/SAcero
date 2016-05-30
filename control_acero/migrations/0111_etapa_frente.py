# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0110_etapa_funcionanterior'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='frente',
            field=models.ForeignKey(to='control_acero.Frente', null=True),
        ),
    ]
