# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0033_remove_frente_estatusfrente'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='nombre',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
