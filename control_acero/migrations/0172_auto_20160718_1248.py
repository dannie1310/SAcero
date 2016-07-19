# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0171_frente_idefolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisicodetallecierre',
            name='folio',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='inventariofisicodetallecierre',
            name='numFolio',
            field=models.IntegerField(null=True),
        ),
    ]
