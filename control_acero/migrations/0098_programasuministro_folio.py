# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0097_auto_20160520_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='programasuministro',
            name='folio',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
