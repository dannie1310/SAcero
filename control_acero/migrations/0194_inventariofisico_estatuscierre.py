# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0193_auto_20160815_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisico',
            name='estatusCierre',
            field=models.IntegerField(default=0, choices=[(0, 'Abierto'), (1, 'Cerrado')]),
        ),
    ]
