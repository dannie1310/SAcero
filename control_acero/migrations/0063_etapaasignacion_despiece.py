# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0062_etapaasignacion_piezasrecibidas'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapaasignacion',
            name='despiece',
            field=models.ForeignKey(to='control_acero.Despiece', null=True),
        ),
    ]
