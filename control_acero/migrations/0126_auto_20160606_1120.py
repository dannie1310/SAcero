# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0125_remisiondetalle_folio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remision',
            name='frente',
            field=models.ForeignKey(to='control_acero.Frente', null=True),
        ),
    ]
