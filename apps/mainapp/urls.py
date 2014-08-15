from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    
    
    url(r'ioe/cps/(?P<exam_code>\w{1,40})/$',
        'apps.mainapp.views.attend_cps_exam'),
    url(r'ioe/dps/(?P<exam_code>\w{1,40})/$',
        'apps.mainapp.views.attend_dps_exam'),
    url(r'answers/(?P<exam_code>\w{1,40})/(?P<subject_name>\w{1,40})/$',
        'apps.mainapp.views.show_result'),
    url(r'list-results/$',
        'apps.mainapp.views.get_list_of_result'),
    url(r'coupon/$', 'apps.mainapp.views.couponpage'),
    url(r'coupons/$', 'apps.mainapp.views.couponspage_redirect'),
    url(r'^ajax-handler/(?P<func_name>\w{1,40})$',
        'apps.mainapp.home.ajax_request', name='ajax_handle'),
    # url(r'^demo/$', 'apps.mainapp.views.demo', name='demo'),
)
