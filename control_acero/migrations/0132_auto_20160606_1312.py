# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0131_auto_20160606_1306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrada',
            options={'permissions': (('add_salida_habilitado', 'Puede ver y agregar Habilitado'), ('change_salida_habilitado', 'Puede cambiar Habilitado'), ('delete_salida_habilitado', 'Puede Borrar Habilitado'))},
        ),
    ]
