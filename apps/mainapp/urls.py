from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^$', 'apps.mainapp.views.landing'),   
    url(r'^/home/$', 'apps.mainapp.views.dashboard'),   
    url(r'honorcode/(?P<exam_code>\w{1,40})/$', 'apps.mainapp.views.honorcode'),
    url(r'cps/(?P<exam_code>\w{1,40})/$', 'apps.mainapp.views.attend_cps_exam'),
    url(r'dps/(?P<exam_code>\w{1,40})/$', 'apps.mainapp.views.attend_dps_exam'),
    url(r'answers/(?P<exam_code>\w{1,40})/(?P<subject_name>\w{1,40})/$','apps.mainapp.views.show_result'),
    url(r'list-results/$','apps.mainapp.views.get_list_of_result'),
    url(r'coupon/$','apps.mainapp.views.couponpage'),
    url(r'^ajax-handler/(?P<func_name>\w{1,40})$', 'apps.mainapp.home.ajax_request', name='ajax_handle'),	
    
)
