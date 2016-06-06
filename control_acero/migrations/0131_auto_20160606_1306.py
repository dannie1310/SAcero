# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0130_auto_20160606_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrada',
            options={'permissions': (('view_task', 'Can see available tasks'), ('change_task_status', 'Can change the status of tasks'), ('close_task', 'Can remove a task by setting its status as closed'))},
        ),
    ]
