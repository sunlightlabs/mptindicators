# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0010_aggregate'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='findings',
            field=models.TextField(blank=True),
        ),
    ]
