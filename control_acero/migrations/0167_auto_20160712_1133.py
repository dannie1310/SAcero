# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0166_auto_20160712_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remision',
            name='ajuste',
            field=models.ForeignKey(related_name='ajusteEntrada', to='control_acero.InventarioFisico', null=True),
        ),
        migrations.AlterField(
            model_name='salida',
            name='ajuste',
            field=models.ForeignKey(related_name='ajusteSalida', to='control_acero.InventarioFisico', null=True),
        ),
    ]
