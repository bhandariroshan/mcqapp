from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mcq.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^add-question/$', 'mainapp.views.add_question'),
    url(r'^add-exam-set/$', 'Exam.views.add_exam_set'),
    url(r'^test/$', 'mainapp.views.dashboard'),
    url(r'^attempt/$', 'mainapp.views.attempt_question'),
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'mainapp.views.landing'),
    
)