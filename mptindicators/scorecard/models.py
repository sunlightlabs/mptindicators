from __future__ import unicode_literals
import random
from collections import defaultdict
from django.db import models
import re

class Region(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2, blank=True)
    region = models.ForeignKey(Region, related_name='countries', blank=True, null=True)
    findings = models.TextField(blank=True)
    electoral_summary = models.TextField(blank=True)

    aggregate_score = models.PositiveSmallIntegerField(blank=True, null=True)
    in_law_score = models.PositiveSmallIntegerField(blank=True, null=True)
    in_practice_score = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name

    def aggregate_score_chart_width(self):
        return self.aggregate_score if self.aggregate_score > 0 else 1

    @property
    def gi_name(self):
        return self.name.lower().replace(' ', '-')


class Section(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=255, blank=True)
    findings = models.TextField(blank=True)

    class Meta:
        ordering = ('number',)

    def __unicode__(self):
        return self.name


class Subsection(models.Model):
    section = models.ForeignKey(Section, related_name="subsections")
    number = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('section__number', 'number')

    def __unicode__(self):
        return '{} / {}'.format(self.section.name, self.name)


class Indicator(models.Model):

    UNKNOWN_TYPE = 0
    IN_LAW_TYPE = 1
    IN_PRACTICE_TYPE = 2
    OPEN_TYPE = 3

    TYPES = (
        (UNKNOWN_TYPE, 'unknown'),
        (IN_LAW_TYPE, 'in law'),
        (IN_PRACTICE_TYPE, 'in practice'),
        (OPEN_TYPE, 'open question'),
    )

    subsection = models.ForeignKey(Subsection, related_name='indicators')
    number = models.PositiveSmallIntegerField(default=0)
    name = models.TextField()
    criteria = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    references = models.TextField(blank=True)
    type = models.PositiveSmallIntegerField(choices=TYPES, default=UNKNOWN_TYPE)

    class Meta:
        ordering = ('number',)

    def __unicode__(self):
        return self.name

    def headerfy_name(self):
        header_hash = defaultdict(lambda: '')
        max_header_length = 63
        for idx, n in enumerate(self.name):
            length_of_current_word = len(re.search("(\S*)", self.name[idx:-1]).groups()[0])
            if idx + length_of_current_word < max_header_length:
                header_hash['header'] += self.name[idx]
            else:
                header_hash['subheader'] += self.name[idx]
        return header_hash

    def header(self):
        return self.headerfy_name()['header']

    def subheader(self):
        return self.headerfy_name()['subheader']

class IndicatorScore(models.Model):
    indicator = models.ForeignKey(Indicator, related_name="indicator_scores")
    country = models.ForeignKey(Country, related_name="indicator_scores")
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True)
    sources = models.TextField(blank=True)

    class Meta:
        ordering = ('country__name', 'indicator__number')

    def score_chart_width(self):
        return self.score if self.score > 0 else 1

    @property
    def rendered_sources(self):
        lines = [l.strip() for l in self.sources.split('\n')]
        return '\n'.join('* {}'.format(l) for l in lines if l)


class Aggregate(models.Model):
    country = models.ForeignKey(Country, related_name="aggregates")
    section = models.ForeignKey(
        Section, related_name="aggregates", blank=True, null=True)
    subsection = models.ForeignKey(
        Subsection, related_name="aggregates", blank=True, null=True)
    score = models.PositiveSmallIntegerField(blank=True, null=True)

    def score_chart_width(self):
        return self.score if self.score > 0 else 1
