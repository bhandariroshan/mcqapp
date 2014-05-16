from django.conf.urls import patterns, url


urlpatterns = patterns(

    '',

    url(r'^$',
        'apps.exam_api.android_api.get_upcoming_exams',
        name='list_exams'),
    url(r'^(?P<exam_code>\d+)',
        'apps.exam_api.android_api.get_question_set',
        name='get_model_question'),
    url(r'^load-questions',
        'apps.exam_api.load_database.load_modelquestion_in_database',
        name='load_model_question'),
    url(r'^load-exam-data',
        'apps.exam_api.load_database.load_examset_in_database',
        name='load_exam_data'),
    url(r'^answers',
        'apps.exam_api.views.check_answers',
        name='check_answers'),
)
