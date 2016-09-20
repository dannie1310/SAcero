# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0201_auto_20160919_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elemento',
            name='tipo',
            field=models.IntegerField(default=0, choices=[(0, 'Un apoyo'), (1, 'Entre apoyos')]),
        ),
    ]
