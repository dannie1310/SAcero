# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0043_auto_20160501_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asignacionetapa',
            name='ControlAsignacion',
        ),
        migrations.RemoveField(
            model_name='asignacionetapa',
            name='funcion',
        ),
        migrations.DeleteModel(
            name='AsignacionEtapa',
        ),
    ]
