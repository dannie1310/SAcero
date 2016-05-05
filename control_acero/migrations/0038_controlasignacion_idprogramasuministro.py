# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0037_programasuministro_programasuministrodetalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlasignacion',
            name='idProgramaSuministro',
            field=models.IntegerField(default=0),
        ),
    ]
