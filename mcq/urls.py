from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(

    '',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^', include('apps.mainapp.urls', app_name='mainapp')),
    url(r'^exam/', include('apps.exam_api.urls', app_name='exam_api')),
)
