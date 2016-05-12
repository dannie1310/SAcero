# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0069_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='tipo',
            field=models.IntegerField(default=1, choices=[(0, 'Certificado'), (1, 'Remision')]),
        ),
    ]
