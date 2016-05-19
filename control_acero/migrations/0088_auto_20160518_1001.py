# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0087_auto_20160518_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='peso',
        ),
    ]
