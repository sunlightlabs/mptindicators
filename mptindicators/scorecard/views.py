from django.shortcuts import render
from django.views.generic import View, DetailView, ListView
from .models import Country, Section, Subsection, Indicator


class MPTView(View):
    def get_context_data(self, **kwargs):
        context = super(MPTView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['sections'] = Section.objects.all()
        return context


class CountryList(MPTView, ListView):
    model = Country


class CountryDetail(MPTView, DetailView):
    model = Country
    slug_field = 'code'
    slug_url_kwarg = 'code'


class IndicatorList(MPTView, ListView):
    model = Indicator


class SectionList(MPTView, ListView):
    model = Section

    def get_queryset(self):
        return Section.objects.prefetch_related("subsections__indicators")


class SectionDetail(MPTView, DetailView):
    model = Section
    slug_field = "number"
    slug_url_kwarg = "section"

    def get_queryset(self):
        return Section.objects.prefetch_related("subsections__indicators")


class SubsectionDetail(MPTView, DetailView):
    model = Subsection
    slug_field = "number"
    slug_url_kwarg = "subsection"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        snum = self.kwargs.get('section', None)
        ssnum = self.kwargs.get('subsection', None)
        return queryset.get(section__number=snum, number=ssnum)

    def get_queryset(self):
        return Subsection.objects.prefetch_related("indicators").select_related("section")

    def get_context_data(self, **kwargs):
        context = super(SubsectionDetail, self).get_context_data(**kwargs)
        context['section'] = self.object.section
        return context


class IndicatorDetail(MPTView, DetailView):
    model = Indicator
    slug_field = "number"
    slug_url_kwarg = "number"

    def get_queryset(self):
        return Indicator.objects.prefetch_related("indicator_scores").select_related("subsection__section")

    def get_context_data(self, **kwargs):
        context = super(IndicatorDetail, self).get_context_data(**kwargs)
        context['subsection'] = self.object.subsection
        context['section'] = self.object.subsection.section
        return context
