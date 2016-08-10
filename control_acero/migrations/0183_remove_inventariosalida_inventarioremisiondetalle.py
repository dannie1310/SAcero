# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0182_inventariosalida_inventarioremisiondetalle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventariosalida',
            name='inventarioRemisionDetalle',
        ),
    ]
