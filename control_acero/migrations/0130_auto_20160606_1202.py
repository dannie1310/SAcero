# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0129_auto_20160606_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='folio',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='numFolio',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='folio',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='numFolio',
            field=models.IntegerField(null=True),
        ),
    ]
