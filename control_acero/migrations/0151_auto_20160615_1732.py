# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0150_apoyo_frente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventarioremisiondetalle',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='inventarioremisiondetalle',
            name='peso',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='remision',
            name='pesoBruto',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='remision',
            name='pesoNeto',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='remision',
            name='pesoTara',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='remisiondetalle',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='remisiondetalle',
            name='peso',
            field=models.IntegerField(null=True),
        ),
    ]
