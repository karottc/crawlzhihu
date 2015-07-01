from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^gethomelist$', 'api.views.GetHomeList'),
    url(r'^getnextlist$', 'api.views.GetNextList'),
    url(r'^getstorydetail$', 'api.views.GetStoryDetail'),
)
