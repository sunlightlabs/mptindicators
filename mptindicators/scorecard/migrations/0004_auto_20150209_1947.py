# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0003_remove_region_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='country',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='score',
        ),
    ]
