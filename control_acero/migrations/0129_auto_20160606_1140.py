# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0128_remisiondetalle_numfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remisiondetalle',
            name='numFolio',
            field=models.IntegerField(null=True),
        ),
    ]
