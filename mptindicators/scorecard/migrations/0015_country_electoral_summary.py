# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0014_auto_20150701_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='electoral_summary',
            field=models.TextField(blank=True),
        ),
    ]
