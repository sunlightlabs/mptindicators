# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0015_country_electoral_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='findings',
            field=models.TextField(blank=True),
        ),
    ]
