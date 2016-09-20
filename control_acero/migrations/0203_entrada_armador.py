# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0202_auto_20160919_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='armador',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
