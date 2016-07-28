# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0180_inventariofisico_numconteo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remision',
            name='idOrden',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
