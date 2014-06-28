from django.conf.urls import patterns, url


urlpatterns = patterns(

    '',

    url(r'^ioe-questions',
        'apps.random_questions.views.generate_random_ioe_questions',
        name='generate_random_ioe_questions'),
)
