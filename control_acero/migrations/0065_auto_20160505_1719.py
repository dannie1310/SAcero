# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0064_etapaasignacion_tipoestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despiece',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
