# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0013_remove_indicator_criteria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indicator',
            old_name='description',
            new_name='criteria',
        ),
    ]
