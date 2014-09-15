import json

from django.http import HttpResponse
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from apps.mainapp.classes.query_database import QuestionApi

from .forms import QuestionForm


class QuestionCreateView(FormView):

    template_name = 'superuser/question_form.html'
    form_class = QuestionForm
    success_url = '/question/add/'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(QuestionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(QuestionCreateView, self).form_valid(form)

# class QuestionUpdateView(View):
#     template_name


def landing(request):
    """This is the landing view for question admin
    """

    parameters = {}
    question_api_object = QuestionApi()
    parameters['exam_type'] = question_api_object.find_distinct_value(
        'exam_type')
    parameters['subject'] = question_api_object.find_distinct_value(
        'subject')
    parameters['exam_code'] = question_api_object.find_distinct_value(
        'exam_code')
    return HttpResponse(json.dumps(parameters))
