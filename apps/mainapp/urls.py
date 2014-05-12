from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'test/$', 'apps.mainapp.views.dashboard'),
    url(r'attempt/$', 'apps.mainapp.views.attempt_question'),
    url(r'^$', 'apps.mainapp.views.landing'),
    url(r'exam/sample/$', 'apps.mainapp.views.exam_sample')
)
