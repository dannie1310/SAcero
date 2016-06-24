# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0157_inventariofisico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventariofisico',
            name='elemento',
        ),
        migrations.RemoveField(
            model_name='inventariofisico',
            name='material',
        ),
        migrations.DeleteModel(
            name='InventarioFisico',
        ),
    ]
