# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0111_etapa_frente'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventarioFisico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('despiece', models.IntegerField()),
                ('elemento', models.IntegerField()),
                ('apoyo', models.IntegerField()),
                ('cantidadFisica', models.IntegerField()),
                ('longitudFisica', models.IntegerField()),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('frente', models.ForeignKey(to='control_acero.Frente')),
                ('proveedor', models.ForeignKey(to='control_acero.Funcion')),
            ],
        ),
        migrations.AddField(
            model_name='elemento',
            name='imagen',
            field=models.FileField(null=True, upload_to='imagen'),
        ),
    ]
