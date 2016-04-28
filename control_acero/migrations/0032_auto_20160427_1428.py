# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0031_auto_20160427_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='longitud',
        ),
        migrations.RemoveField(
            model_name='material',
            name='nombre',
        ),
    ]
