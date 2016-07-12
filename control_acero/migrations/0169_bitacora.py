# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('control_acero', '0168_modulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accion', models.CharField(max_length=100)),
                ('id_afectado', models.IntegerField()),
                ('observacion', models.CharField(max_length=200)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('modulo', models.ForeignKey(to='control_acero.Modulo')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
