from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'apps.mainapp.views.landing'),
    url(r'^latex-store$', 'apps.mainapp.views.add_html'),
    url(r'^latex$', 'apps.mainapp.views.latex_html'),
    url(r'^home/$', 'apps.mainapp.views.dashboard'),
    url(r'^generate-coupon/$', 'apps.mainapp.views.generate_coupon'),
    url(r'^get-coupons/(?P<subscription_type>\w{1,15})/$', 'apps.mainapp.views.get_coupons'),
    url(r'^terms/$', 'apps.mainapp.views.tos'),
    url(r'^privacy/$', 'apps.mainapp.views.privacy'),
    url(r'^android/$', 'apps.mainapp.views.android'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('apps.mainapp.urls', app_name='mainapp')),
    url(r'^exam/', include('apps.exam_api.urls', app_name='exam_api')),
    url(r'^subscription/', 'apps.mainapp.views.subscription'),
    url(r'^results/(?P<exam_code>\w{1,15})', 'apps.mainapp.views.results'),
)
