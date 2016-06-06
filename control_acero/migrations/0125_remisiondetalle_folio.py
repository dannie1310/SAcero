# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0124_auto_20160603_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='remisiondetalle',
            name='folio',
            field=models.IntegerField(null=True),
        ),
    ]
