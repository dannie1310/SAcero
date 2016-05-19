# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0073_material_longitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='longitud',
            field=models.IntegerField(null=True),
        ),
    ]
