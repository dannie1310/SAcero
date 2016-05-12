# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0065_auto_20160505_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programasuministro',
            name='fechaFinal',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='programasuministro',
            name='fechaInicial',
            field=models.DateField(),
        ),
    ]
