# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0116_auto_20160602_1335'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Grupo',
        ),
        migrations.DeleteModel(
            name='Modulo',
        ),
    ]
