# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0009_country_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aggregate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('country', models.ForeignKey(related_name='aggregates', to='scorecard.Country')),
                ('section', models.ForeignKey(related_name='aggregates', blank=True, to='scorecard.Section', null=True)),
                ('subsection', models.ForeignKey(related_name='aggregates', blank=True, to='scorecard.Subsection', null=True)),
            ],
        ),
    ]
