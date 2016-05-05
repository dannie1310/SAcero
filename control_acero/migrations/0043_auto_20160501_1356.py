# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0042_auto_20160501_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlasignacion',
            name='idProgramaSuministro',
        ),
        migrations.RemoveField(
            model_name='controlasignacion',
            name='idProgramaSuministroDetalle',
        ),
        migrations.AddField(
            model_name='controlasignacion',
            name='programaSuministro',
            field=models.ForeignKey(to='control_acero.ProgramaSuministro', null=True),
        ),
        migrations.AddField(
            model_name='controlasignacion',
            name='programaSuministroDetalle',
            field=models.ForeignKey(to='control_acero.ProgramaSuministroDetalle', null=True),
        ),
    ]
