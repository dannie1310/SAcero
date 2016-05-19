# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0090_auto_20160518_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='programaSuministro',
        ),
        migrations.AddField(
            model_name='etapaasignacion',
            name='programaSuministroDetalle',
            field=models.ForeignKey(to='control_acero.ProgramaSuministroDetalle', null=True),
        ),
    ]
