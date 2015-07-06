import re

import markdown2
from django.conf import settings
from django.db import models

from . import validators


class Page(models.Model):

    path = models.CharField(max_length=255)
    template = models.CharField(max_length=255, default='pages/simplepage.html')
    is_published = models.BooleanField(default=False)

    title = models.CharField(max_length=255)
    intro = models.TextField(blank=True)
    content = models.TextField(blank=True)
    sidebar = models.TextField(blank=True)

    js = models.TextField(blank=True)
    css = models.TextField(blank=True)

    class Meta:
        ordering = ('path',)

    def __unicode__(self):
        return self.path

    def get_absolute_url(self):
        return self.path

    def rendered_content(self):
        return markdown2.markdown(self.content)

    def save(self, **kwargs):
        super(Page, self).save(**kwargs)

    def save(self, **kwargs):
        self.path = "/%s/" % self.path.strip("/")
        super(Page, self).save(**kwargs)


class Chunk(models.Model):

    slug = models.SlugField()
    content = models.TextField(blank=True)

    class Meta:
        ordering = ('slug',)

    def __unicode__(self):
        return self.slug

    def rendered(self):
        return markdown2.markdown(self.content)
