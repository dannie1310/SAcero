# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0199_remision_pesoremision'),
    ]

    operations = [
        migrations.AddField(
            model_name='salida',
            name='estatusApoyo',
            field=models.IntegerField(default=0, choices=[(2, 'Doble'), (1, 'Un')]),
        ),
    ]
