# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0121_auto_20160603_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='elemento',
            field=models.ForeignKey(to='control_acero.Elemento', null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='elemento',
            field=models.ForeignKey(to='control_acero.Elemento', null=True),
        ),
    ]
