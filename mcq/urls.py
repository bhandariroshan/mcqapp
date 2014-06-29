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
    url(r'^androidlogin/$', 'apps.mainapp.views.android'),
    url(r'^android/$', 'apps.mainapp.views.androidapk'),
    url(r'^privacy/$', 'apps.mainapp.views.privacy'),
    url(r'^notifications/$', 'apps.mainapp.views.notifications'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('apps.mainapp.urls', app_name='mainapp')),
    url(r'^exam/', include('apps.exam_api.urls', app_name='exam_api')),
    url(r'^subscription/', 'apps.mainapp.views.subscription'),
    url(r'^distributors/', 'apps.mainapp.views.distributors'),
    url(r'^request/', 'apps.mainapp.views.request_coupon'),
    url(r'^results/(?P<exam_code>\w{1,15})', 'apps.mainapp.views.results'),
    url(r'^latestusers/$','apps.mainapp.latest_users.latest_users'),
    url(r'^coupon_admin/$', 'apps.exam_api.coupon_admin.coupon_search'),    
    url(r'^iom/$', 'apps.mainapp.views.iomdashboard'),
    url(r'^iom/(?P<exam_code>\w{1,15})/$', 'apps.mainapp.views.attend_IOM_dps_exam'),
    url(r'^random/', include('apps.random_questions.urls', app_name='random_questions')),
)
