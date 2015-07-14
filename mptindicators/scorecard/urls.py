from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .models import Country, Section
from .views import (CountryList, CountryDetail, SectionList,
    IndicatorList, SectionDetail, SubsectionDetail, IndicatorDetail,
    CountryData, IndexView)


class MPTTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(MPTTemplateView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['sections'] = Section.objects.all()
        return context


urlpatterns = [
    url(r'^countries/$',
        CountryList.as_view(), name='scorecard_countries'),
    url(r'^countries/(?P<code>[\w-]+)/$',
        CountryDetail.as_view(), name='scorecard_country'),
    url(r'^countries/(?P<code>[\w-]+)/data/$',
        CountryData.as_view(), name='scorecard_country_data'),
    url(r'^indicators/$',
        IndicatorList.as_view(), name='scorecard_indicators'),
    url(r'^sections/$',
        SectionList.as_view(), name='scorecard_sections'),
    url(r'^sections/(?P<section>\d)/$',
        SectionDetail.as_view(), name='scorecard_section'),
    url(r'^sections/4/1.*',
        SectionDetail.as_view(), {'pk': 4}),
    url(r'^sections/(?P<section>\d)/(?P<subsection>\d)/$',
        SubsectionDetail.as_view(), name='scorecard_subsection'),
    url(r'^indicators/(?P<number>\d{1,2})/$',
        IndicatorDetail.as_view(), name='scorecard_indicator'),
]


# static view

urlpatterns += [
    url(r'^contributors/$', MPTTemplateView.as_view(
        template_name='scorecard/contributors.html'), name='scorecard_contributors'),
    url(r'^faq/$', MPTTemplateView.as_view(
        template_name='scorecard/faq.html'), name='scorecard_faq'),
    url(r'^methodology/$', MPTTemplateView.as_view(
        template_name='scorecard/methodology.html'), name='scorecard_methodology'),
    url(r'^$', IndexView.as_view(), name='scorecard'),
]
