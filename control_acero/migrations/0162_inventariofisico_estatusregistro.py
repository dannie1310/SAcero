# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0161_auto_20160623_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisico',
            name='estatusRegistro',
            field=models.IntegerField(default=0, choices=[(0, 'Abierto'), (1, 'Cerrado')]),
        ),
    ]
