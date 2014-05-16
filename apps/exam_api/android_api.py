import json

from django.http import HttpResponse

from .views import ExamHandler


def get_question_set(request, exam_code):
    '''
    the function returns the api of a model question
    '''
    exam_handler = ExamHandler()
    model_question_set = exam_handler.get_questionset_from_database(
        exam_code)
    return HttpResponse(json.dumps(model_question_set))


def get_upcoming_exams(request):
    '''
    the function returns api of upcoming exams
    '''
    exam_handler = ExamHandler()
    upcoming_exams = exam_handler.list_upcoming_exams()
    return HttpResponse(json.dumps(upcoming_exams))


def get_scores(request):
    '''
    the function returns api of scores obtained in each subject
    '''
    if request.method == 'GET':
        exam_code = request.GET.get('exam')
        answer_list = list(request.GET.get('answers'))
        exam_handler = ExamHandler()
        score_dict = exam_handler.check_answers(exam_code, answer_list)
        return HttpResponse(json.dumps(score_dict))
    else:
        return HttpResponse('Not a valid request')
