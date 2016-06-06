# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0127_auto_20160606_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='remisiondetalle',
            name='numFolio',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
