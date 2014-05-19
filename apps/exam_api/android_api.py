import json

from django.http import HttpResponse

from .views import ExamHandler
from apps.mainapp.classes.Coupon import Coupon

def get_question_set(request, exam_code):
    '''
    the function returns the api of a model question
    '''
    if request.user.is_authenticated():
        exam_handler = ExamHandler()
        model_question_set = exam_handler.get_questionset_from_database(
            exam_code)
        return HttpResponse(json.dumps(model_question_set))
    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'Not a valid request'}))


def get_upcoming_exams(request):
    '''
    the function returns api of upcoming exams
    '''
    if request.user.is_authenticated():
        exam_handler = ExamHandler()
        upcoming_exams = exam_handler.list_upcoming_exams()
        return HttpResponse(json.dumps(upcoming_exams))
    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'Not a valid request'}))



def get_scores(request):
    '''
    the function returns api of scores obtained in each subject
    '''
    if request.user.is_authenticated():
        if request.method == 'GET':
            exam_code = request.GET.get('exam')
            answer_list = list(request.GET.get('answers'))
            exam_handler = ExamHandler()
            score_dict = exam_handler.check_answers(exam_code, answer_list)
            return HttpResponse(json.dumps(score_dict))
    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'Not a valid request'}))

def validate_coupon(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            coupon_code = request.GET.get('coupon_code','')
            exam_code = request.GET.get('exam_code','')
            coupon_obj = Coupon()
            coupon = coupon_obj.validate_coupon(coupon_code)
            if coupon != None:
                coupon_obj.change_used_status_of_coupon(coupon_code, request.user.id, exam_code)
                return HttpResponse(json,dumps({'status':'ok', 'coupon_code':coupon_code, 'subscription_type':coupon['subscription_type']}))
            else:
                return HttpResponse(json.dumps({'status':'error', 'message':'Invalid Coupon'}))
            
    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'Not a valid request'}))