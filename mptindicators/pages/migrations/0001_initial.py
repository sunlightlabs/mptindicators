# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('content', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=255)),
                ('template', models.CharField(default=b'pages/simplepage.html', max_length=255)),
                ('is_published', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('intro', models.TextField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('sidebar', models.TextField(blank=True)),
                ('js', models.TextField(blank=True)),
                ('css', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('path',),
            },
        ),
    ]
