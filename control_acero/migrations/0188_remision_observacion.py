# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0187_auto_20160810_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='remision',
            name='observacion',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
