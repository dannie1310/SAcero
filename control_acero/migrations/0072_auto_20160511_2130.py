# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0071_archivo_typoarchivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archivo',
            old_name='typoArchivo',
            new_name='tipoArchivo',
        ),
    ]
