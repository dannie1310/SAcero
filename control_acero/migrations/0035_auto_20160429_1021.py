# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0034_material_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frente',
            name='identificacion',
            field=models.CharField(max_length=100),
        ),
    ]
