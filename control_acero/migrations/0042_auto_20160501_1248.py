# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0041_auto_20160501_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlasignacion',
            name='idElementoMaterial',
        ),
        migrations.AddField(
            model_name='controlasignacion',
            name='idProgramaSuministroDetalle',
            field=models.IntegerField(default=0),
        ),
    ]
