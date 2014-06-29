from django.conf.urls import patterns, url


urlpatterns = patterns(

    '',

    url(r'^ioe-questions',
        'apps.random_questions.views.generate_random_ioe_questions',
        name='generate_random_ioe_questions'),
    url(r'^load-question-id',
        'apps.random_questions.views.add_questions_in_exam_model',
        name='add_questions_in_exam_model'),
)
