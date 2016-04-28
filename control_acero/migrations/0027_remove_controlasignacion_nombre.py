# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0026_controlasignacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlasignacion',
            name='nombre',
        ),
    ]
