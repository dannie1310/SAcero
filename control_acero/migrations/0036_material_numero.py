# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0035_auto_20160429_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='numero',
            field=models.IntegerField(default=0),
        ),
    ]
