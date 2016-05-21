# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0095_auto_20160520_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='imagen',
            field=models.FileField(null=True, upload_to='imagenes/materiales/'),
        ),
    ]
