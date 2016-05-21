# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0094_auto_20160519_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('cantidad', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('tiempoEntrega', models.IntegerField(null=True)),
                ('cantidadAsignada', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('idEtapaPertenece', models.IntegerField(null=True)),
                ('estatusEtapa', models.IntegerField()),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('tipoEstatus', models.IntegerField(default=1, choices=[(1, 'En proceso'), (2, 'Recepcionado'), (3, 'Enviado'), (4, 'Rechazado')])),
                ('tipoRecepcion', models.IntegerField(default=1, choices=[(0, 'Parcial'), (1, 'Total')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EtapaDespiece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('despieceTotal', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('pesoRecibido', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('pesoRestante', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('cantidad', models.IntegerField(null=True)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EtapaDespieceDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('despiecePeso', models.DecimalField(default=Decimal('0.000'), null=True, max_digits=20, decimal_places=3)),
                ('estatus', models.IntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')])),
                ('fechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('despiece', models.ForeignKey(to='control_acero.Despiece')),
            ],
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='EtapaAsignacionDespiece',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='funcion',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='programaSuministro',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='programaSuministroDetalle',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='taller',
        ),
        migrations.RemoveField(
            model_name='etapaasignacion',
            name='transporte',
        ),
        migrations.RemoveField(
            model_name='etapaasignaciondespiece',
            name='EtapaAsignacionDespieceDetalle',
        ),
        migrations.RemoveField(
            model_name='etapaasignaciondespiece',
            name='elemento',
        ),
        migrations.RemoveField(
            model_name='etapaasignaciondespiece',
            name='material',
        ),
        migrations.RemoveField(
            model_name='etapaasignaciondespiecedetalle',
            name='despiece',
        ),
        migrations.RemoveField(
            model_name='archivo',
            name='etapaAsignacion',
        ),
        migrations.DeleteModel(
            name='EtapaAsignacion',
        ),
        migrations.DeleteModel(
            name='EtapaAsignacionDespiece',
        ),
        migrations.DeleteModel(
            name='EtapaAsignacionDespieceDetalle',
        ),
        migrations.AddField(
            model_name='etapadespiece',
            name='EtapaDespieceDetalle',
            field=models.ManyToManyField(to='control_acero.EtapaDespieceDetalle', blank=True),
        ),
        migrations.AddField(
            model_name='etapadespiece',
            name='elemento',
            field=models.ForeignKey(to='control_acero.Elemento'),
        ),
        migrations.AddField(
            model_name='etapadespiece',
            name='material',
            field=models.ForeignKey(to='control_acero.Material'),
        ),
        migrations.AddField(
            model_name='etapa',
            name='EtapaDespiece',
            field=models.ManyToManyField(to='control_acero.EtapaDespiece', blank=True),
        ),
        migrations.AddField(
            model_name='etapa',
            name='funcion',
            field=models.ForeignKey(to='control_acero.Funcion'),
        ),
        migrations.AddField(
            model_name='etapa',
            name='programaSuministro',
            field=models.ForeignKey(to='control_acero.ProgramaSuministro', null=True),
        ),
        migrations.AddField(
            model_name='etapa',
            name='programaSuministroDetalle',
            field=models.ForeignKey(to='control_acero.ProgramaSuministroDetalle', null=True),
        ),
        migrations.AddField(
            model_name='etapa',
            name='taller',
            field=models.ForeignKey(to='control_acero.Taller', null=True),
        ),
        migrations.AddField(
            model_name='etapa',
            name='transporte',
            field=models.ForeignKey(to='control_acero.Transporte', null=True),
        ),
        migrations.AddField(
            model_name='archivo',
            name='etapa',
            field=models.ForeignKey(to='control_acero.Etapa', null=True),
        ),
    ]
