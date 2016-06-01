# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0112_auto_20160530_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapadespiece',
            name='elemento',
            field=models.ForeignKey(to='control_acero.Elemento', null=True),
        ),
        migrations.AlterField(
            model_name='etapadespiece',
            name='material',
            field=models.ForeignKey(to='control_acero.Material', null=True),
        ),
    ]
