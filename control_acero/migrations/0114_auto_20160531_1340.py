# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0113_auto_20160531_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapa',
            name='funcion',
            field=models.ForeignKey(to='control_acero.Funcion', null=True),
        ),
    ]
