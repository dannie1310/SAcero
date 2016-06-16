# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0149_auto_20160614_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='apoyo',
            name='frente',
            field=models.ForeignKey(to='control_acero.Frente', null=True),
        ),
    ]
