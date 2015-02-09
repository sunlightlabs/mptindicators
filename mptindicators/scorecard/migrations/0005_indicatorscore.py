# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0004_auto_20150209_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('country', models.ForeignKey(related_name='indicator_scores', to='scorecard.Country')),
                ('indicator', models.ForeignKey(related_name='indicator_scores', to='scorecard.Indicator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
