# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0051_auto_20160502_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transporte',
            name='tipo',
            field=models.IntegerField(default=1, choices=[(1, 'Local'), (2, 'Tercero')]),
        ),
    ]
