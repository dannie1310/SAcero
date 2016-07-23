# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0178_auto_20160721_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisicodetallecompleto',
            name='estatusDetalle',
            field=models.IntegerField(default=0, choices=[(0, 'Pendiente'), (1, 'Activo')]),
        ),
    ]
