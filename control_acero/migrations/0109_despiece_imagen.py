# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0108_auto_20160526_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='despiece',
            name='imagen',
            field=models.FileField(null=True, upload_to='despieces'),
        ),
    ]
