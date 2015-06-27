from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'west.views.first_page'),
    url(r'^staff$', 'west.views.staff'),
)
