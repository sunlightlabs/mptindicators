# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField(default=0)),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('references', models.TextField(blank=True)),
                ('score', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('country', models.ForeignKey(related_name='indicators', to='scorecard.Country')),
            ],
            options={
                'ordering': ('number',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('score', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('number',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('section', models.ForeignKey(related_name='subsections', to='scorecard.Section')),
            ],
            options={
                'ordering': ('section__number', 'number'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='indicator',
            name='subsection',
            field=models.ForeignKey(related_name='indicators', to='scorecard.Subsection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(related_name='countries', to='scorecard.Region'),
            preserve_default=True,
        ),
    ]
