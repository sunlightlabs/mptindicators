# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0007_auto_20150602_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='aggregate_score',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='country',
            name='in_law_score',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='country',
            name='in_practice_score',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
