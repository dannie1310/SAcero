# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0080_delete_frenteasigna'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programasuministrodetalle',
            old_name='numeroCinco',
            new_name='peso',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='idProgramaSuministro',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroCuatro',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroDiez',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroDoce',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroNueve',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroOcho',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroOnce',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroSeis',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='numeroSiete',
        ),
        migrations.RemoveField(
            model_name='programasuministrodetalle',
            name='total',
        ),
        migrations.AddField(
            model_name='programasuministrodetalle',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='programasuministrodetalle',
            name='material',
            field=models.ForeignKey(to='control_acero.Material', null=True),
        ),
        migrations.AddField(
            model_name='programasuministrodetalle',
            name='programaSuministro',
            field=models.ForeignKey(to='control_acero.ProgramaSuministro', null=True),
        ),
    ]
