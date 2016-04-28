# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0028_asignacionetapa'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrenteAsigna',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idOrden', models.IntegerField(null=True, blank=True)),
                ('idFrente', models.IntegerField(blank=True)),
                ('tipo', models.IntegerField()),
                ('idEstructuraElemento', models.IntegerField()),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
