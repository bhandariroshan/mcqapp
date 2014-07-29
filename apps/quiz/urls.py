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
        r'^(?P<exam_type>\w{1,40})/$',
        view=SingleQuizView.as_view(),
        name='single_quiz'
    ),
)
