# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0138_inventarioremisiondetalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioremisiondetalle',
            name='estatusTotalizado',
            field=models.IntegerField(default=1),
        ),
    ]
