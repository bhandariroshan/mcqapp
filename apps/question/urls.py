from django.conf.urls import patterns, url

from .views import QuestionCreateView

urlpatterns = patterns(

    '',

    url(r'^$',
        'apps.question.views.landing',
        name='question_landing'),

    url(r'^add/$',
        QuestionCreateView.as_view(),
        name='add_question'),

    # url(r'^(?P<question_id>[-\w]+)/$',
    #     'apps.question.views.question_update_ui',
    #     name='question_update_ui'),
)
