# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0123_auto_20160603_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='remision',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='remision',
            field=models.IntegerField(null=True),
        ),
    ]
