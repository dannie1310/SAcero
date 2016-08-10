# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0181_auto_20160728_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariosalida',
            name='inventarioRemisionDetalle',
            field=models.ManyToManyField(to='control_acero.InventarioRemisionDetalle', blank=True),
        ),
    ]
