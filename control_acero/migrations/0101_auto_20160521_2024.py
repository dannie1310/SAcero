# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0100_etapa_folio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etapa',
            name='folio',
        ),
        migrations.RemoveField(
            model_name='programasuministro',
            name='folio',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='folio',
        ),
    ]
