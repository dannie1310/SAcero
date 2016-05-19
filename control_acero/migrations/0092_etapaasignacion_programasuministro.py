# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0091_auto_20160518_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapaasignacion',
            name='programaSuministro',
            field=models.ForeignKey(to='control_acero.ProgramaSuministro', null=True),
        ),
    ]
