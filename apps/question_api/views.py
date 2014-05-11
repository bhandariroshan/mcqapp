import json

from django.http import HttpResponse

from .query_question_database import QuestionApi


def load_questionset_in_database(request):
    '''
    the function is used to load fake data in question collection
    of mcq database in mongodb
    '''
    f = open('apps/question_api/question_testdata.json', 'rb')
    json_obj = json.loads(f.read())
    question_api = QuestionApi()
    question_api.insert_new_question(json_obj)
    return HttpResponse("Question saved in the database")


def load_examinfo_in_database(request):


def get_upcoming_exams(request):
    '''
    the function returns the list of exam sets
    that can be attended
    '''
    question_api = QuestionApi()
    upcoming_exams = question_api.find_all


def get_questionset_from_database(request, exam_code):
    '''
    This function returns the questions with same examcode
    '''
    question_api = QuestionApi()
    questions = question_api.find_all({"exam_code": exam_code})
    return HttpResponse(json.dumps(questions))


# def check_answers(request, answer_list):
