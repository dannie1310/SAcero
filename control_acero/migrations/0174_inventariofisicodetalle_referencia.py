# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0173_inventariofisicodetallecierre_tallerasignado'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisicodetalle',
            name='referencia',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
