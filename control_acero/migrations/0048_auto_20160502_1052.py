# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0047_auto_20160502_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapaasignacion',
            name='taller',
            field=models.ForeignKey(to='control_acero.Taller', null=True),
        ),
    ]
