from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mcq.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^add-question/$', 'apps.mainapp.views.add_question'),
    url(r'^add-exam-set/$', 'apps.Exam.views.add_exam_set'),
    url(r'^test/$', 'apps.mainapp.views.dashboard'),
    url(r'^attempt/$', 'apps.mainapp.views.attempt_question'),
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'apps.mainapp.views.landing'),
    
)