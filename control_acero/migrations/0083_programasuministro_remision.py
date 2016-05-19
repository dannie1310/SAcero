# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0082_programasuministrodetalle_longitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='programasuministro',
            name='remision',
            field=models.IntegerField(null=True),
        ),
    ]
