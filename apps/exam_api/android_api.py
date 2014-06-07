import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile

from .views import ExamHandler


@csrf_exempt
def get_question_set(request, exam_code):
    '''
    the function returns the api of a model question
    '''
    if request.user.is_authenticated():
        coupon_code = request.POST.get('coupon')
        user_obj = UserProfile()
        from apps.mainapp.classes.Exams import Exam
        exam_obj = Exam()

        up_exm = exam_obj.get_exam_detail(int(exam_code))
        coupon_obj = Coupon()
        user_profile_obj = UserProfile()
        subscription_status = user_obj.check_subscribed(request.user.username,
                                                        exam_code
                                                        )
        user = user_profile_obj.get_user_by_username(request.user.username)

        '''Validation for subscription here'''
        if subscription_status or int(exam_code) in user['valid_exam']:
            exam_handler = ExamHandler()
            model_question_set = exam_handler.get_questionset_from_database(
                exam_code)

            if len(model_question_set) > 0:
                return HttpResponse(json.dumps(
                    {'status': 'ok', 'result': model_question_set})
                )
            else:
                return HttpResponse(json.dumps(
                    {'status': 'error',
                     'message': 'No question in this exam right now.'
                     }
                )
                )

        if coupon_obj.validate_coupon(coupon_code, up_exm['exam_category'],
                                      up_exm['exam_family']) is True:

            user_profile_obj = UserProfile()
            user_profile_obj.change_subscription_plan(request.user.username,
                                                      coupon_code)
            #save the coupon code in user's couponcode array
            coupon_obj.change_used_status_of_coupon(coupon_code,
                                                    request.user.username)
            user_profile_obj.save_coupon(request.user.username, coupon_code)

            subscription_status = user_obj.check_subscribed(
                request.user.username, exam_code
            )
            if subscription_status:
                '''Add Validation for subscription here'''
                exam_handler = ExamHandler()
                model_question_set = exam_handler.\
                    get_questionset_from_database(exam_code)

                response = HttpResponse(json.dumps(
                    {'status': 'ok', 'result': model_question_set}
                )
                )
            else:
                response = HttpResponse(json.dumps(
                    {'status': 'error',
                     'message': 'You are not subscribed for this exam'}
                )
                )
        else:
            response = HttpResponse(json.dumps(
                {'status': 'error', 'message': 'Invalid Coupon Code.'}
            )
            )
    else:
        response = HttpResponse(json.dumps(
            {'status': 'error', 'message': 'Not a valid request'}
        )
        )
    return response


def get_upcoming_exams(request):
    '''
    the function returns api of upcoming exams
    '''
    if request.user.is_authenticated():
        exam_handler = ExamHandler()
        upcoming_exams = exam_handler.list_upcoming_exams()
        for eachExam in upcoming_exams:
            user_obj = UserProfile()
            subscription_status = user_obj.check_subscribed(
                request.user.username, eachExam['exam_code']
            )
            eachExam['subscribed'] = 1 if subscription_status else 0

        return HttpResponse(json.dumps(
            {'status': 'ok', 'result': upcoming_exams}
        )
        )
    else:
        return HttpResponse(json.dumps(
            {'status': 'error', 'message': 'Not a valid request'}
        )
        )


@csrf_exempt
def get_scores(request):
    '''
    the function returns api of scores obtained in each subject
    '''
    if request.user.is_authenticated():
        IMPROPER_REQUEST = 'Couldn\'t process improper request'
        try:
            exam_code = int(request.POST['exam_code'])
            answer_list = list(request.POST['answers'])
        except Exception:
            return HttpResponse(json.dumps(
                {'status': 'error', 'message': IMPROPER_REQUEST}
            )
            )

        from apps.mainapp.classes.query_database import AttemptedAnswerDatabase, QuestionApi
        question_obj = QuestionApi() 
        ans = AttemptedAnswerDatabase()
        questions = question_obj.find_all_questions({"exam_code": int(exam_code)})        
        sorted_questions = sorted(questions, key=lambda k: k['question_number'])
        attempt_time = time.mktime(datetime.datetime.now().timetuple())

        for i in range(0,len(answer_list)):
            ans.update_upsert_push({
                'user_id':request.user.id,
                'ess_time':int(attempt_time),
                'attempt_device':'android',
                'q_id':sorted_questions[i]['uid']['id'],
                'exam_code':int(exam_code),
                'q_no':i},{
                'attempt_details':{
                    'selected_ans':eachAns,
                    'attempt_time':int(attempt_time)
                }})

        exam_handler = ExamHandler()                
        score_dict = exam_handler.check_answers(exam_code, answer_list)
        return HttpResponse(json.dumps(
            {'status': 'ok', 'result': score_dict}
        )
        )
    else:
        return HttpResponse(json.dumps(
            {'status': 'error', 'message': 'Not a valid request'}
        )
        )


def validate_coupon(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            coupon_code = request.GET.get('coupon_code', '')
            exam_code = request.GET.get('exam_code', '')
            coupon_obj = Coupon()
            coupon = coupon_obj.validate_coupon(coupon_code)
            if coupon is not None:
                coupon_obj.change_used_status_of_coupon(
                    coupon_code, request.user.id, exam_code
                )
                return HttpResponse(json.dumps(
                    {'status': 'ok',
                     'coupon_code': coupon_code,
                     'subscription_type': coupon['subscription_type']}
                )
                )
            else:
                return HttpResponse(json.dumps(
                    {'status': 'error', 'message': 'Invalid Coupon'}
                )
                )

    else:
        return HttpResponse(json.dumps(
            {'status': 'error', 'message': 'Not a valid request'}
        )
        )
