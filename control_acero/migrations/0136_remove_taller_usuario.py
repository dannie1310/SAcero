# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0135_auto_20160607_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taller',
            name='usuario',
        ),
    ]
