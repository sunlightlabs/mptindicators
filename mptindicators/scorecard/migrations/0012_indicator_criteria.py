# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0011_country_findings'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='criteria',
            field=models.TextField(blank=True),
        ),
    ]
