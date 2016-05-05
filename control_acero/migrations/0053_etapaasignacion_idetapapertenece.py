# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0052_auto_20160502_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapaasignacion',
            name='idEtapaPertenece',
            field=models.IntegerField(null=True),
        ),
    ]
