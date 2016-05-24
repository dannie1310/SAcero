# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0099_programasuministrodetalle_folio'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='folio',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
