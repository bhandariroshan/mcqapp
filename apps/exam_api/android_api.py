import datetime
import time
import json
from bson.objectid import ObjectId

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.mainapp.classes.Exams import Exam
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
from apps.mainapp.classes.query_database import ExammodelApi, AttemptedAnswerDatabase, QuestionApi
from apps.random_questions.views import generate_random_ioe_questions, generate_random_iom_questions

from .views import ExamHandler


def get_question_set_for_android(exam_code):
    '''
    This function returns the questions of for a exam model
    by checking the exam_code for android with correct answer
    '''
    exammodel_api = ExammodelApi()
    try:
        exam_model = exammodel_api.find_one_exammodel(
            {"exam_code": int(exam_code)}
        )
        question_id_list = [
            ObjectId(i['id']) for i in exam_model['question_list']
        ]
        question_api = QuestionApi()
        question_list = question_api.find_all_questions(
            {
                '_id': {"$in": question_id_list}
            }
        )
        sorted_questions = sorted(
            question_list, key=lambda k: k['question_number'])
        return sorted_questions

    except:
        pass


@csrf_exempt
def get_question_set(request, exam_code):
    '''
    the function returns the api of a model question
    '''
    exam_code = int(exam_code)
    if request.user.is_authenticated():
        coupon_code = request.POST.get('coupon')
        user_profile_obj = UserProfile()

        exam_obj = Exam()
        coupon_obj = Coupon()

        user = user_profile_obj.get_user_by_username(request.user.username)
        subscription = False
        if "IDP" in user['subscription_type']:
            subscription = True

        '''
        if exam_code is 0 then new IOE set is generated randomly and
        the newly generated exam_code is used to access questions.
        '''
        if exam_code == 0:
            if "BE-IOE" in user['subscription_type']:
                subscription = True
            if not subscription and not coupon_obj.validate_coupon(coupon_code, 'BE-IOE', 'DPS'):
                response = HttpResponse(
                    json.dumps(
                        {'status': 'error', 'message': 'Invalid Coupon Code.'}
                    )
                )
                return response
            else:
                exam_code = generate_random_ioe_questions(request)
                user_profile_obj.save_valid_exam(
                    user['username'], int(exam_code)
                )

        '''
        if exam_code is 1 then new IOM set is generated randomly and
        the newly generated exam_code is used to access questions.
        '''
        if exam_code == 1:
            if "MBBS-IOM" in user['subscription_type']:
                subscription = True
            if not subscription and not coupon_obj.validate_coupon(coupon_code, 'MBBS-IOM', 'DPS'):
                response = HttpResponse(
                    json.dumps(
                        {'status': 'error', 'message': 'Invalid Coupon Code.'}
                    )
                )
                return response
            else:
                exam_code = generate_random_iom_questions(request)
                user_profile_obj.save_valid_exam(
                    user['username'], int(exam_code)
                )
        up_exm = exam_obj.get_exam_detail(int(exam_code))
        if up_exm['exam_family'] == 'CPS':
            if time.mktime(datetime.datetime.now().timetuple()) < up_exm['exam_date']:
                return HttpResponse(
                    json.dumps(
                        {'status': 'error',
                         'message': 'Exam has not begin yet, please check back later.'}
                    )
                )

        subscription_status = user_profile_obj.check_subscribed(
            request.user.username, exam_code
        )

        '''Validation for subscription here'''
        if subscription_status or int(exam_code) in user['valid_exam']:
            model_question_set = get_question_set_for_android(
                exam_code
            )

            if len(model_question_set) > 0:
                return HttpResponse(json.dumps(
                    {'status': 'ok',
                     'result': model_question_set,
                     'exam_model_code': exam_code})
                )
            else:
                return HttpResponse(json.dumps(
                    {'status': 'error',
                     'message': 'No question in this exam right now.'
                     }
                )
                )

        if coupon_obj.validate_coupon(coupon_code, up_exm['exam_category'], up_exm['exam_family']) is True:

            user_profile_obj.change_subscription_plan(request.user.username,
                                                      coupon_code)
            #save the coupon code in user's couponcode array
            coupon_obj.change_used_status_of_coupon(coupon_code,
                                                    request.user.username)
            user_profile_obj.save_coupon(request.user.username, coupon_code)

            subscription_status = user_profile_obj.check_subscribed(
                request.user.username, exam_code
            )
            if subscription_status:
                '''Add Validation for subscription here'''
                model_question_set = get_question_set_for_android(
                    exam_code
                )
                response = HttpResponse(json.dumps(
                    {'status': 'ok',
                     'result': model_question_set,
                     'exam_model_code': exam_code}
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
        user_obj = UserProfile()
        usr = user_obj.get_user_by_username(request.user.username)
        '''
        check full subscription of user
        return subscription status of exam_category for the user`
        '''
        subscribed_ioe = 0
        subscribed_iom = 0
        if "BE-IOE" in usr['subscription_type']:
            subscribed_ioe = 1
        elif "MBBS-IOM" in usr['subscription_type']:
            subscribed_iom = 1
        elif "IDP" in usr['subscription_type']:
            subscribed_ioe = subscribed_iom = 1
        user_exams = usr['valid_exam']
        upcoming_exams = []
        for count, eachExam in enumerate(user_exams):
            exam_model_api = ExammodelApi()
            up_exam = exam_model_api.find_one_exammodel(
                {'exam_code': eachExam}, {'question_list': 0}
            )
            if up_exam is None:
                continue

            elif up_exam['exam_category'] == 'BE-IOE':
                up_exam['exam_date'] = int(up_exam['exam_date'])
                up_exam['exam_name'] = 'IOE Practice Exam ' + str(count + 1)
                up_exam['subscribed'] = 1
                upcoming_exams.append(up_exam)

            elif up_exam['exam_category'] == 'MBBS-IOM':
                up_exam['exam_date'] = int(up_exam['exam_date'])
                up_exam['exam_name'] = 'IOM Practice Exam ' + str(count + 1)
                up_exam['subscribed'] = 1
                upcoming_exams.append(up_exam)

        return HttpResponse(json.dumps(
            {'status': 'ok',
             'result': upcoming_exams[::-1],
             'subscribed_ioe': subscribed_ioe,
             'subscribed_iom': subscribed_iom}
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
        IMPROPER_REQUEST = 'Could not process improper request'
        try:
            exam_code = int(request.POST['exam_code'])
            answer_list = list(request.POST['answers'])
        except Exception:
            return HttpResponse(json.dumps(
                {'status': 'error', 'message': IMPROPER_REQUEST}
            )
            )
        exam_handler = ExamHandler()
        exam_obj = ExammodelApi()
        exam_details = exam_obj.find_one_exammodel(
            {'exam_code': int(exam_code)}
        )
        question_list = get_question_set_for_android(int(exam_code))
        ans = AttemptedAnswerDatabase()
        attempt_time = time.mktime(datetime.datetime.now().timetuple())
        if exam_details['exam_family'] == 'CPS':
            if (attempt_time - (exam_details['exam_date'] + exam_details['exam_duration'] * 60)) > 15 * 60:
                return HttpResponse(json.dumps(
                    {'status': 'error',
                     'message': 'We are sorry, you are late in submitting your answers.'}))

        for i in range(0, len(answer_list)):
            ans.update_upsert_push({
                'user_id': request.user.id,
                'ess_time': int(attempt_time),
                'attempt_device': 'android',
                'q_id': question_list[i]['uid']['id'],
                'exam_code': int(exam_code),
                'q_no': i},
                {'attempt_details': {
                 'selected_ans': answer_list[i],
                 'attempt_time': int(attempt_time)
                 }})

        score_dict = exam_handler.save_exam_result(request, exam_details, attempt_time)
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
