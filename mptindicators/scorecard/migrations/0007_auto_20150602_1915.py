# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0006_auto_20150602_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicatorscore',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='indicatorscore',
            name='sources',
            field=models.TextField(blank=True),
        ),
    ]
