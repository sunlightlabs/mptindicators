import random
from collections import defaultdict
from django.db import models


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


class Section(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=255, blank=True)

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


class IndicatorScore(models.Model):
    indicator = models.ForeignKey(Indicator, related_name="indicator_scores")
    country = models.ForeignKey(Country, related_name="indicator_scores")
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True)
    sources = models.TextField(blank=True)

    class Meta:
        ordering = ('country__name', 'indicator__number')


class Aggregate(models.Model):
    country = models.ForeignKey(Country, related_name="aggregates")
    section = models.ForeignKey(
        Section, related_name="aggregates", blank=True, null=True)
    subsection = models.ForeignKey(
        Subsection, related_name="aggregates", blank=True, null=True)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
