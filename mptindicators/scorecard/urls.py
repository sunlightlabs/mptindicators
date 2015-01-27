from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^countries/(?P<slug>[\w-]+)/$', 'mptindicators.views.home', name='scorecard_countries'),
)
