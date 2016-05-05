# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0061_auto_20160504_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapaasignacion',
            name='piezasRecibidas',
            field=models.IntegerField(null=True),
        ),
    ]
