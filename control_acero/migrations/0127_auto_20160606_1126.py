# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0126_auto_20160606_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remisiondetalle',
            name='folio',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
