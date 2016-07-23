# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0176_auto_20160721_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventarioremisiondetalle',
            name='estatusTipoV',
        ),
        migrations.AddField(
            model_name='inventariofisicodetalle',
            name='estatusTipoV',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'No Habilitada'), (2, 'Proceso'), (3, 'Habilitada')]),
        ),
    ]
