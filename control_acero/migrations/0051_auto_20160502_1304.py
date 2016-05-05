# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0050_etapaasignacion_programasuministro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcion',
            name='tipo',
            field=models.IntegerField(default=1, choices=[(1, 'Suministrador'), (2, 'Habilitador'), (3, 'Armador'), (4, 'Colocador')]),
        ),
    ]
