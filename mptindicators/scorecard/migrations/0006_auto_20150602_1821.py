# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0005_indicatorscore'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicatorscore',
            options={'ordering': ('country__name', 'indicator__number')},
        ),
        migrations.AddField(
            model_name='indicator',
            name='type',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, b'unknown'), (1, b'in law'), (2, b'in practice'), (3, b'open question')]),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
