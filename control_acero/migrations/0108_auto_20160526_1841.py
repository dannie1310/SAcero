# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0107_etapa_material'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etapa',
            name='programaSuministro',
        ),
        migrations.RemoveField(
            model_name='etapa',
            name='programaSuministroDetalle',
        ),
        migrations.AddField(
            model_name='etapa',
            name='idOrdenTrabajo',
            field=models.IntegerField(null=True),
        ),
    ]
