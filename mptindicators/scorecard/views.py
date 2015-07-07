import unicodecsv as csv
from contextlib import closing
from cStringIO import StringIO
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, ListView, TemplateView
from django.utils.text import slugify
from .models import Country, Section, Subsection, Indicator


class MPTView(View):
    def get_context_data(self, **kwargs):
        context = super(MPTView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['sections'] = Section.objects.all()
        return context


class IndexView(MPTView, TemplateView):

    template_name = 'scorecard/index.html'

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        qs = context['countries']

        ordering = self.request.GET.get('o')

        if ordering == 'name_asc':
            qs = qs.order_by('name')
        if ordering == 'name_desc':
            qs = qs.order_by('-name')
        if ordering == 'score_asc':
            qs = qs.order_by('aggregate_score', 'name')
        if ordering == 'score_desc':
            qs = qs.order_by('-aggregate_score', 'name')

        context['ordering'] = ordering
        context['indicator_countries'] = qs

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
        qs = Indicator.objects.prefetch_related(
            "indicator_scores").select_related("subsection__section")
        return qs

    def get_context_data(self, **kwargs):

        context = super(IndicatorDetail, self).get_context_data(**kwargs)
        context['subsection'] = self.object.subsection
        context['section'] = self.object.subsection.section

        ordering = self.request.GET.get('o')
        indicator_scores = self.object.indicator_scores.all()

        if ordering == 'name_asc':
            indicator_scores = indicator_scores.order_by('country__name')
        if ordering == 'name_desc':
            indicator_scores = indicator_scores.order_by('-country__name')
        if ordering == 'score_asc':
            indicator_scores = indicator_scores.order_by('score', 'country__name')
        if ordering == 'score_desc':
            indicator_scores = indicator_scores.order_by('-score', 'country__name')

        context['ordering'] = ordering
        context['indicator_scores'] = indicator_scores

        return context


#
# data download views
#

class CountryData(DetailView):

    def get(self, request, *args, **kwargs):
        country = get_object_or_404(Country, code=kwargs['code'])

        with closing(StringIO()) as bffr:

            writer = csv.writer(bffr)

            writer.writerow(
                ('indicator', 'question', 'type', 'score',
                 'section', 'section_name', 'subsection', 'subsection_name'))

            for score in country.indicator_scores.select_related():

                indicator = score.indicator
                subsection = indicator.subsection
                section = subsection.section

                row = (
                    indicator.number,
                    indicator.name,
                    indicator.get_type_display(),
                    score.score,
                    section.number,
                    section.name,
                    subsection.number,
                    subsection.name,
                )

                writer.writerow(row)

            content = bffr.getvalue()

        filename = 'indicators_{}.csv'.format(slugify(country.name))

        resp = HttpResponse(content, content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        return resp




