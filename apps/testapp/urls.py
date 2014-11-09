from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',       
    url(r'test/dps/(?P<exam_code>\w{1,40})/$',
        'apps.mainapp.views.attend_dps_exam'),

    url(r'test/(?P<subject_name>\w{1,40})/$',
        'apps.testapp.views.subject_wise_test_ui'),

    url(r'test/start/(?P<subject_name>\w{1,40})/$',
        'apps.testapp.views.attend_subject_wise_test'),   

    # url(r'^demo/$', 'apps.mainapp.views.demo', name='demo'),
)