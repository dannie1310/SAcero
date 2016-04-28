# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0029_frenteasigna'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apoyo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=100)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('elemento', models.ManyToManyField(to='control_acero.Elemento')),
            ],
        ),
        migrations.RemoveField(
            model_name='estructura',
            name='elemento',
        ),
        migrations.DeleteModel(
            name='Estructura',
        ),
    ]
