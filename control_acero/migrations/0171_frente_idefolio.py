# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0170_auto_20160713_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='frente',
            name='ideFolio',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
