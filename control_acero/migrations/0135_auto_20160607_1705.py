# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('control_acero', '0134_auto_20160607_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='tallerAsignado',
            field=models.ForeignKey(related_name='tallerAsignadoEntrada', to='control_acero.Taller', null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='tallerAsignado',
            field=models.ForeignKey(related_name='tallerAsignadoSalida', to='control_acero.Taller', null=True),
        ),
        migrations.AddField(
            model_name='taller',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
