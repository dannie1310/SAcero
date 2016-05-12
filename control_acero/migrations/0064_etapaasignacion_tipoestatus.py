# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0063_etapaasignacion_despiece'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapaasignacion',
            name='tipoEstatus',
            field=models.IntegerField(default=1, choices=[(1, 'En proceso'), (2, 'Recepcionado'), (3, 'Enviado'), (4, 'Rechazado')]),
        ),
    ]
