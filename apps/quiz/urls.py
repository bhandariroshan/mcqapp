from django.conf.urls import patterns, url
from .views import QuizView, SingleQuizView, QuizGenerate, QuizScore, AjaxRequest
from .quiz_result_admin import QuizResultAdminView

urlpatterns = patterns(
    '',
    url(
        r'^$',
        view=QuizView.as_view(),
        name='quiz_home'
    ),

    url(
        r'^generate/(?P<exam_type>\w{1,40})/$',
        view=QuizGenerate.as_view(),
        name='generate_quiz'
    ),

    url(
        r'^myscore/$',
        view=QuizScore.as_view(),
        name='my_score'),


    url(
        r'^quiz-ajax/(?P<func_name>\w{1,40})$',
        AjaxRequest.as_view(),
        name='quiz_ajax',
    ),

    url(
        r'^winners/$',
        QuizResultAdminView.as_view(),
        name='quiz_winner',
    ),

    url(
        r'^(?P<exam_category>[-\w]+)/$',
        view=SingleQuizView.as_view(),
        name='single_quiz'
    ),

)
