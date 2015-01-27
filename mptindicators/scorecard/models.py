from django.db import models


class Region(models.Model):
	name = models.CharField(max_length=255)
	score = models.PositiveSmallIntegerField(blank=True, null=True)

	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return self.name


class Country(models.Model):
	slug = models.SlugField()
	name = models.CharField(max_length=255)
	score = models.PositiveSmallIntegerField(blank=True, null=True)
	region = models.ForeignKey(Region, related_name='countries')

	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return self.name


class Section(models.Model):
	number = models.PositiveSmallIntegerField(default=0)
	name = models.CharField(max_length=255)

	class Meta:
		ordering = ('number',)

	def __unicode__(self):
		return self.name


class Subsection(models.Model):
	section = models.ForeignKey()
	number = models.PositiveSmallIntegerField(default=0)
	name = models.CharField(max_length=255, related_name='subsections')

	class Meta:
		ordering = ('section.number', 'number')

	def __unicode__(self):
		return '{} / {}'.format(self.section.name, self.name)


class Indicator(models.Model):
	number = models.PositiveSmallIntegerField(default=0)
	name = models.TextField()
	description = models.TextField(blank=True)
	comment = models.TextField(blank=True)
	references = models.TextField(blank=True)
	country = models.ForeignKey(Country, related_name='indicators')
	subsection = models.ForeignKey(Subsection, related_name='indicators')
	score = models.PositiveSmallIntegerField(blank=True, null=True)

	class Meta:
		ordering = ('number',)

	def __unicode__(self):
		return self.name
		
