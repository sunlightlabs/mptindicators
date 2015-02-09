from django.conf.urls import patterns, include, url
from .views import (CountryList, CountryDetail,
    IndicatorList, SectionDetail, SubsectionDetail, IndicatorDetail)


urlpatterns = patterns('',
    url(r'^countries/$', CountryList.as_view(), name='scorecard_countries'),
    url(r'^countries/(?P<slug>[\w-]+)/$', CountryDetail.as_view(), name='scorecard_country'),
    url(r'^indicators/$', IndicatorList.as_view(), name='scorecard_indicators'),
    url(r'^indicators/(?P<section>\d)/$', SectionDetail.as_view(), name='scorecard_section'),
    url(r'^indicators/(?P<section>\d)/(?P<subsection>\d)/$', SubsectionDetail.as_view(), name='scorecard_subsection'),
    url(r'^indicators/(?P<section>\d)/(?P<subsection>\d)/(?P<number>\d{1,2})/$', IndicatorDetail.as_view(), name='scorecard_indicator'),
)
