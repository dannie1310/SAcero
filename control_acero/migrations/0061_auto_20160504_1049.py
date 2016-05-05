# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0060_elemento_despiece'),
    ]

    operations = [
        migrations.RenameField(
            model_name='despiece',
            old_name='nombre',
            new_name='nomenclatura',
        ),
        migrations.RemoveField(
            model_name='despiece',
            name='calibre',
        ),
        migrations.RemoveField(
            model_name='despiece',
            name='pieza',
        ),
        migrations.RemoveField(
            model_name='despiece',
            name='pija',
        ),
        migrations.AddField(
            model_name='despiece',
            name='cantidad',
            field=models.IntegerField(default=1, max_length=20),
        ),
        migrations.AddField(
            model_name='despiece',
            name='fechaActualizacion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='despiece',
            name='figura',
            field=models.CharField(default=1, max_length=20),
        ),
        migrations.AddField(
            model_name='despiece',
            name='peso',
            field=models.DecimalField(default=Decimal('0.0000'), null=True, max_digits=20, decimal_places=4),
        ),
    ]
