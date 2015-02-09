from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Country, Section, Subsection, Indicator


class CountryList(ListView):
    model = Country


class CountryDetail(DetailView):
    model = Country

    def get_context_data(self, **kwargs):
        context = super(CountryDetail, self).get_context_data(**kwargs)
        context["countries"] = Country.objects.all()
        return context


class IndicatorList(ListView):
    model = Indicator


class SectionList(ListView):
    model = Section

    def get_queryset(self):
        return Section.objects.prefetch_related("subsections__indicators")


class SectionDetail(DetailView):
    model = Section
    slug_field = "number"
    slug_url_kwarg = "section"

    def get_queryset(self):
        return Section.objects.prefetch_related("subsections__indicators")

    def get_context_data(self, **kwargs):
        context = super(SectionDetail, self).get_context_data(**kwargs)
        context["sections"] = self.get_queryset()
        return context


class SubsectionDetail(DetailView):
    model = Subsection
    slug_field = "number"
    slug_url_kwarg = "subsection"

    def get_queryset(self):
        return Subsection.objects.prefetch_related("indicators").select_related("section")

    def get_context_data(self, **kwargs):
        context = super(SubsectionDetail, self).get_context_data(**kwargs)
        context["sections"] = Section.objects.prefetch_related("subsections__indicators")
        return context


class IndicatorDetail(DetailView):
    model = Indicator
    slug_field = "number"
    slug_url_kwarg = "number"

    def get_queryset(self):
        return Indicator.objects.prefetch_related("indicator_scores").select_related("subsection__section")

    def get_context_data(self, **kwargs):
        context = super(IndicatorDetail, self).get_context_data(**kwargs)
        context["sections"] = Section.objects.prefetch_related("subsections__indicators")
        return context
