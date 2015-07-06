from django.shortcuts import render, get_object_or_404
from .models import Page


def page(request, path):
    path = "/%s/" % path.strip('/')
    p = get_object_or_404(Page, path=path, is_published=True)
    context = {
        "page": p
    }
    return render(request, p.template, context)
