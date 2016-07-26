# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0179_inventariofisicodetallecompleto_estatusdetalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariofisico',
            name='numConteo',
            field=models.IntegerField(null=True),
        ),
    ]
