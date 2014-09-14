import json

from bson.objectid import ObjectId
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.mainapp.classes.query_database import QuestionApi

from .forms import QuestionForm


def add_question(request):
    parameters = RequestContext(request)
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        parameters['question_form'] = question_form
        if question_form.is_valid():
            new_form = question_form.save()
            print new_form
            return HttpResponseRedirect('/')
        else:
            parameters['question_form'] = question_form
            render_to_response('superuser/question_form.html', parameters)
    else:
        question_form = QuestionForm()
        parameters['question_form'] = question_form
        return render_to_response('superuser/question_form.html', parameters)


def question_update_ui(request, question_id):
    """ This view is used to update any question in the database
    """

    question_api_object = QuestionApi()
    selected_question = question_api_object.find_one_question(
        {'_id': ObjectId(question_id)})
    return HttpResponse(json.dumps(selected_question))


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
