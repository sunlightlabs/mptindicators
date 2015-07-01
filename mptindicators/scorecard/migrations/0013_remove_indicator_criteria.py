# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0012_indicator_criteria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='criteria',
        ),
    ]
