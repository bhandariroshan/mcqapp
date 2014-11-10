from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^$', 'apps.mainapp.views.set_category', name="set_category"),
    url(r'^$', 'apps.mainapp.views.new_dashboard', name="new_dashboard"),
    url(r'^(?P<exam_type>ioe|iom)/$', 'apps.mainapp.views.user_dashboard', name="user_dashboard"),
    url(r'^latex-store$', 'apps.mainapp.views.add_html'),
    url(r'^latex-get-data/$', 'apps.mainapp.views.get_all_questions'),
    url(r'^latex$', 'apps.mainapp.views.latex_html'),
    url(r'^dashboard$', 'apps.mainapp.views.new_dashboard'),
    url(r'^generate-coupon/(?P<subscription_type>\w{1,15})/$',
        'apps.mainapp.views.generate_coupon'),
    url(r'^get-coupons/(?P<subscription_type>\w{1,15})/$',
        'apps.mainapp.views.get_coupons'),
    url(r'^terms/$', 'apps.mainapp.views.tos'),
    url(r'^androidlogin/$', 'apps.mainapp.views.android'),
    url(r'^android/$', 'apps.mainapp.views.androidapk'),
    url(r'^privacy/$', 'apps.mainapp.views.privacy'),
    url(r'^notifications/$', 'apps.mainapp.views.notifications'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('apps.mainapp.urls', app_name='mainapp')),
    url(r'^exam/', include('apps.exam_api.urls', app_name='exam_api')),
    url(r'^', include('apps.testapp.urls', app_name='testapp')),
    url(r'^subscription/', 'apps.mainapp.views.subscription'),
    url(r'^distributors/', 'apps.mainapp.views.distributors'),
    url(r'^request/', 'apps.mainapp.views.request_coupon'),
    url(r'^results/(?P<exam_code>\w{1,15})', 'apps.mainapp.views.results'),
    url(r'^latestusers/$', 'apps.mainapp.latest_users.latest_users'),
    url(r'^coupon_admin/$', 'apps.exam_api.coupon_admin.coupon_search'),
    url(r'^subscribe_exam/$',
        'apps.exam_api.coupon_admin.subscribe_user_to_exam'),
    url(r'^iom/dps/(?P<exam_code>\w{1,15})/$',
        'apps.mainapp.views.attend_dps_exam'),
    url(r'^moe/dps/(?P<exam_code>\w{1,15})/$',
        'apps.mainapp.views.attend_dps_exam'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url=settings.STATIC_URL + 'images/logos/favicon.ico')
        ),
    url(r'^robots\.txt$',
        TemplateView.as_view(
            template_name='robots.txt', content_type='text/plain'
        ), name='robots'),
    url(r'^random/',
        include(
            'apps.random_questions.urls', app_name='random_questions'
        )),
    url(r'^quiz/',
        include(
            'apps.quiz.urls', app_name='quiz'
        )),
    url(r'^paying_users/$', 'apps.exam_api.coupon_admin.paying_users'),
    url(r'^history/$', 'apps.mainapp.views.history'),
    url(r'^history/(?P<subject_name>\w{1,30})/$', 'apps.mainapp.views.subject_history'),


    # url(r'^mongonaut/', include('mongonaut.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
