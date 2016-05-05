# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0040_controlasignacion_elemento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlasignacion',
            name='elemento',
        ),
        migrations.AddField(
            model_name='controlasignacion',
            name='idElementoMaterial',
            field=models.IntegerField(null=True),
        ),
    ]
