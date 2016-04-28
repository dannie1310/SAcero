# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0024_auto_20160418_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despiece',
            name='material',
            field=models.ManyToManyField(to='control_acero.Material', blank=True),
        ),
    ]
