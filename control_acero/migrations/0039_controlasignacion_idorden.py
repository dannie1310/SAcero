# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0038_controlasignacion_idprogramasuministro'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlasignacion',
            name='idOrden',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
