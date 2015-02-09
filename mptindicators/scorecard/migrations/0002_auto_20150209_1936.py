# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterField(
            model_name='country',
            name='region',
            field=models.ForeignKey(related_name='countries', blank=True, to='scorecard.Region', null=True),
            preserve_default=True,
        ),
    ]
