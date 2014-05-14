from django.conf.urls import patterns, url


urlpatterns = patterns(

    '',

    url(r'^$',
        'apps.exam_api.views.list_exam_set',
        name='list_exams'),
    url(r'^(?P<exam_code>\d+)',
        'apps.exam_api.views.get_questionset_from_database',
        name='get_model_question'),
    url(r'^load-questions',
        'apps.exam_api.views.load_modelquestion_in_database',
        name='load_model_question'),
    url(r'^load-exam-data',
        'apps.exam_api.views.load_examset_in_database',
        name='load_exam_data'),
<<<<<<< HEAD
    url(r'^$',
        'apps.exam_api.views.list_exam_set',
        name='list_exams'),
=======
    url(r'^answers',
        'apps.exam_api.views.check_answers',
        name='check_answers'),
>>>>>>> 9837e30d1d58290ef39690eb31c4708a7805e2a3
)
