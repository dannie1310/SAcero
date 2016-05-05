# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0039_controlasignacion_idorden'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlasignacion',
            name='elemento',
            field=models.ForeignKey(to='control_acero.Elemento', null=True),
        ),
    ]
