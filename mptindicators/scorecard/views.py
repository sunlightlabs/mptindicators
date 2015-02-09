from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Country, Section, Subsection, Indicator


class CountryList(ListView):
    model = Country


class CountryDetail(DetailView):
    model = Country


class IndicatorList(ListView):
    model = Indicator


class SectionDetail(DetailView):
    model = Section


class SubsectionDetail(DetailView):
    model = Subsection


class IndicatorDetail(DetailView):
    model = Indicator
