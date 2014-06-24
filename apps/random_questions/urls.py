from django.conf.urls import patterns, url


urlpatterns = patterns(

    '',

    url(r'^questions',
        'apps.random_questions.views.generate_random_questions',
        name='generate_random_questions'),
)
