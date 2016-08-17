# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0194_inventariofisico_estatuscierre'),
    ]

    operations = [
        migrations.AddField(
            model_name='salida',
            name='estatusReposicion',
            field=models.IntegerField(default=0, choices=[(2, 'No'), (1, 'Si')]),
        ),
    ]
