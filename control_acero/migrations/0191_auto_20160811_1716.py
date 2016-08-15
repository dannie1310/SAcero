# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0190_auto_20160811_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventariofisicodetallecompleto',
            name='referencia',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
