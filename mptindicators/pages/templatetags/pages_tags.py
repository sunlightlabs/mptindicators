from django import template
from ..models import Chunk

register = template.Library()


@register.simple_tag
def chunk(slug):
    try:
        c = Chunk.objects.get(slug=slug)
        return c.rendered()
    except Chunk.DoesNotExist:
        return ''
