# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0172_auto_20160718_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisicodetallecierre',
            name='tallerAsignado',
            field=models.ForeignKey(related_name='tallerAsignadoInventarioCierre', to='control_acero.Taller', null=True),
        ),
    ]
