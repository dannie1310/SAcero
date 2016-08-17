# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0196_auto_20160816_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remision',
            name='pesoTotal',
        ),
    ]
