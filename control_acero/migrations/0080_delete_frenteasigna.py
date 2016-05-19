# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0079_delete_ingenieria'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FrenteAsigna',
        ),
    ]
