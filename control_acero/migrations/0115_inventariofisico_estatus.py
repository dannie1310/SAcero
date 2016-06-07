# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0112_auto_20160528_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisico',
            name='estatus',
            field=models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')]),
        ),
    ]
