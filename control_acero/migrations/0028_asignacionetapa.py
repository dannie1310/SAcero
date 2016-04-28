# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0027_remove_controlasignacion_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionEtapa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estatusEtapa', models.IntegerField()),
                ('etapa', models.IntegerField()),
                ('ControlAsignacion', models.ForeignKey(to='control_acero.ControlAsignacion')),
                ('funcion', models.ForeignKey(to='control_acero.Funcion')),
            ],
        ),
    ]
