# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0106_etapadescuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='material',
            field=models.ForeignKey(to='control_acero.Material', null=True),
        ),
    ]
