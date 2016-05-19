# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0075_auto_20160512_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pva', models.IntegerField()),
                ('factorPulgada', models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4)),
                ('pi', models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True, null=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
