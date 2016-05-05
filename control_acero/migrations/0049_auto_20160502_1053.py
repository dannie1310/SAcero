# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0048_auto_20160502_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapaasignacion',
            name='transporte',
            field=models.ForeignKey(to='control_acero.Transporte', null=True),
        ),
    ]
