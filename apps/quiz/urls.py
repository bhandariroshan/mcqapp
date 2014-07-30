from django.conf.urls import patterns, url
from .views import QuizView, SingleQuizView


urlpatterns = patterns(
    '',
    url(
        r'^$',
        view=QuizView.as_view(),
        name='quiz_home'
    ),
    url(
        r'^generate/(?P<exam_type>\w{1,40})/$', 
        'apps.quiz.views.generate_quiz'
    ),
    url(
        r'^(?P<exam_category>[-\w]+)/$',
        view=SingleQuizView.as_view(),
        name='single_quiz'
    ),
    url(r'^quiz-ajax/(?P<func_name>\w{1,40})$',
        'apps.quiz.views.ajax_request', name='quiz_ajax'),
)
