# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0115_inventariofisico_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='elemento',
            name='imagen',
            field=models.FileField(null=True, upload_to='imagen'),
        ),
    ]
