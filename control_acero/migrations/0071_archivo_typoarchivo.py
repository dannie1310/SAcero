# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0070_archivo_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='typoArchivo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
