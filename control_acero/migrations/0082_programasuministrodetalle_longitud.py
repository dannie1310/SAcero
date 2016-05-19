# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0081_auto_20160516_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='programasuministrodetalle',
            name='longitud',
            field=models.IntegerField(null=True),
        ),
    ]
