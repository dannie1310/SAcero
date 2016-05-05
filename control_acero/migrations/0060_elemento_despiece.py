# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0059_auto_20160503_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='elemento',
            name='despiece',
            field=models.ManyToManyField(to='control_acero.Despiece', blank=True),
        ),
    ]
