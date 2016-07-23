# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0175_auto_20160718_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioremisiondetalle',
            name='estatusTipoV',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'No Habilitada'), (2, 'Proceso'), (3, 'Habilitada')]),
        ),
        migrations.AddField(
            model_name='remisiondetalle',
            name='estatusTipo',
            field=models.IntegerField(default=0, choices=[(0, 'No'), (1, 'Recta'), (2, 'Rollo')]),
        ),
    ]
