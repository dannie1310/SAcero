# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0165_inventariofisicodetallecierre'),
    ]

    operations = [
        migrations.AddField(
            model_name='remision',
            name='ajuste',
            field=models.ForeignKey(related_name='ajusteEntrada', to='control_acero.InventarioFisicoDetalleCierre', null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='ajuste',
            field=models.ForeignKey(related_name='ajusteSalida', to='control_acero.InventarioFisicoDetalleCierre', null=True),
        ),
    ]
