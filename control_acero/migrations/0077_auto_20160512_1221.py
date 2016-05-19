# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0076_factores'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Factores',
            new_name='Factor',
        ),
        migrations.AddField(
            model_name='material',
            name='factor',
            field=models.ForeignKey(to='control_acero.Factor', null=True),
        ),
    ]
