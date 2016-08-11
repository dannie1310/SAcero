# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0189_auto_20160811_0949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taller',
            old_name='proveedor',
            new_name='identificacionFolio',
        ),
    ]
