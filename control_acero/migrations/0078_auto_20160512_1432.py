# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0077_auto_20160512_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='extension',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='archivo',
            name='nombreArchivo',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
