# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0096_material_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='imagen',
            field=models.FileField(null=True, upload_to='materiales'),
        ),
    ]
