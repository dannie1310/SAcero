# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0163_auto_20160705_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventariofisico',
            old_name='toneladaEntradas',
            new_name='totalEntradas',
        ),
        migrations.RenameField(
            model_name='inventariofisico',
            old_name='toneladaSalida',
            new_name='totalSalidas',
        ),
    ]
