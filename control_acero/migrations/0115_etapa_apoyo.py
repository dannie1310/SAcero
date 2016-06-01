# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0114_auto_20160531_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='apoyo',
            field=models.ForeignKey(to='control_acero.Apoyo', null=True),
        ),
    ]
