# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0045_etapaasignacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlasignacion',
            name='tiempoEntrega',
            field=models.IntegerField(null=True),
        ),
    ]
