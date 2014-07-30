# Create your views here.
import json
import datetime
import time

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from apps.random_questions.views import generate_random_ioe_questions, generate_random_iom_questions
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile

from apps.exam_api.views import ExamHandler
from apps.mainapp.classes.Exams import Exam
from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi,\
    ExamStartSignal, HonorCodeAcceptSingal, AttemptedAnswerDatabase,\
    CurrentQuestionNumber

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


class AjaxHandle():
    """doc string for AjaxHandle"""
    def __init__(self):
        pass

    def validate_coupon(self, request):
        if request.user.is_authenticated():
            coupon_obj = Coupon()
            exam_code = request.POST.get('exam_code', '')
            coupon_code = request.POST.get('coupon_code', '')
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            exam_obj = Exam()
            if exam_code != 'subs':
                up_exm = exam_obj.get_exam_detail(int(exam_code))
            else:
                if coupon_obj.has_susbcription_plan_in_coupon(coupon_code):
                    coupon_obj.change_used_status_of_coupon(
                        coupon_code, request.user.username
                    )
                    user_profile_obj.change_subscription_plan(
                        request.user.username, coupon_code
                    )
                    user_profile_obj.save_coupon(
                        request.user.username, coupon_code
                    )
                    return HttpResponse(
                        json.dumps(
                            {'status': 'ok', 'url': '/'}
                        )
                    )
                else:
                    return HttpResponse(
                        json.dumps(
                            {'status': 'error',
                             'message': 'Invalid Coupon code.'}
                        )
                    )

            if coupon_obj.validate_coupon(
                coupon_code,
                up_exm['exam_category'],
                up_exm['exam_family']
            ) is True:
                #save the coupon code in user's coupon code array
                user_profile_obj.change_subscription_plan(
                    request.user.username, coupon_code
                )
                user_profile_obj.save_coupon(
                    request.user.username, coupon_code
                )
                #Refreshment of user
                user = user_profile_obj.get_user_by_username(
                    request.user.username
                )
                subscription_type = user['subscription_type']
                # if coupon_code != 'IDP' or 'BE-IOE' or 'MBBS-IOM' then save
                # the exam code in the valid exams
                if 'IDP' not in subscription_type and 'BE-IOE' not in \
                        subscription_type and 'MBBS-IOM' not in \
                        subscription_type:
                    user_profile_obj.save_valid_exam(
                        request.user.username, exam_code
                    )

                coupon_obj.change_used_status_of_coupon(
                    coupon_code, request.user.username
                )
                if 'IDP' in subscription_type:
                    return HttpResponse(
                        json.dumps(
                            {'status': 'ok',
                             'url': '/' + up_exm['exam_family'].lower() + '/' +
                             exam_code}
                        )
                    )

                elif up_exm['exam_category'] in subscription_type:
                    if up_exm['exam_category'] != 'MBBS-IOM':
                        return HttpResponse(
                            json.dumps(
                                {'status': 'ok',
                                 'url': '/' + up_exm['exam_family'].lower() +
                                 '/' + exam_code}
                            )
                        )
                    else:
                        return HttpResponse(
                            json.dumps(
                                {'status': 'ok',
                                 'url': '/' + 'iom' + '/' + exam_code}
                            )
                        )
                else:
                    subscribed_exams = user_profile_obj.get_subscribed_exams(
                        request.user.username
                    )
                    if int(exam_code) in subscribed_exams:
                        #Check if exam is cps or dps
                        #if exam is cps then return url '/cps/exam_code'
                        #else return  url '/dps/exam_code/'
                        exm_dtls = exam_obj.get_exam_detail(int(exam_code))
                        if exm_dtls['exam_category'] != 'MBBS-IOM':
                            return HttpResponse(
                                json.dumps(
                                    {'status': 'ok',
                                     'url': '/' +
                                     exm_dtls['exam_family'].lower() + '/' +
                                     exam_code}
                                )
                            )
                        else:
                            return HttpResponse(
                                json.dumps(
                                    {'status': 'ok',
                                     'url': '/' + 'iom' + '/' + exam_code}
                                )
                            )
                    else:
                        return HttpResponse(
                            json.dumps(
                                {'status': 'error',
                                 'message': 'Invalid Coupon code.'}
                            )
                        )
            else:
                return HttpResponse(
                    json.dumps(
                        {'status': 'error',
                         'message': 'Invalid Coupon code.'}
                    )
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'You are not authorized to \
                     perform this action.'}
                )
            )

    def is_subscribed(self, request):
        if request.user.is_authenticated():
            coupon_obj = Coupon()
            exam_code = request.POST.get('exam_code', '')
            user_id = request.user.id

            if exam_code.strip() == 'sample':
                return HttpResponse(
                    json.dumps(
                        {'status': 'error', 'message': 'not subscribed'}
                    )
                )
            else:
                if coupon_obj.check_subscried(exam_code, user_id):
                    return HttpResponse(
                        json.dumps(
                            {'status': 'ok',
                             'url': '/honorcode/' + exam_code + '/'}
                        )
                    )
                else:
                    return HttpResponse(
                        json.dumps(
                            {'status': 'error', 'message': 'not subscribed'}
                        )
                    )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'You are not authorized to perform \
                     this action.'}
                )
            )

    def save_answer(self, request):
        if request.user.is_authenticated():
            from apps.exam_api.views import save_user_answers
            ess = ExamStartSignal()
            exam_code = request.POST.get('exam_code', '')
            validate = ess.check_exam_started(
                {'exam_code': int(exam_code),
                 'useruid': request.user.id,
                 'start': 1,
                 'end': 0}
            )
            if validate is not None:
                ema = ExammodelApi()
                exam_details = ema.find_one_exammodel(
                    {'exam_code': int(exam_code)}
                )
                if exam_details['exam_family'] == 'CPS':
                    time_elapsed = time.mktime(
                        datetime.datetime.now().timetuple()
                    ) - exam_details['exam_date']
                else:
                    time_elapsed = time.mktime(
                        datetime.datetime.now().timetuple()
                    ) - validate['start_time']
                time_remained = (
                    exam_details['exam_duration'] * 60 - time_elapsed
                ) / 60
                '''check if user time has expired or not '''
                if time_elapsed > exam_details['exam_duration'] * 60:
                    return HttpResponse(
                        json.dumps(
                            {'status': 'TimeElapsedError',
                             'message': 'Time has elapsed'}
                        )
                    )
                else:
                    save_user_answers(request, int(validate['start_time']))
                    # if request.session.get('has_commented', False):
                    cqn = CurrentQuestionNumber()
                    cqn.update_current_question_number({
                        'ess_time': int(validate['start_time']),
                        'exam_code': int(exam_code),
                        'useruid': request.user.id
                    },
                        {'cqn': int(request.POST.get(
                            'current_question_number', '')
                        ) + 1
                        })
                    request.session['exam_code'] = request.POST.get(
                        'exam_code', ''
                    )
                    return HttpResponse(
                        json.dumps(
                            {'status': 'ok',
                             'message': 'Answer successfully saved',
                             'time_remained': time_remained}
                        )
                    )

            else:
                return HttpResponse(
                    json.dumps(
                        {'status': 'error', 'message': 'Exam not Validated'}
                    )
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'Not Authorized for this action'}
                )
            )


    def honor_code_accept(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code', '')
            request.session[exam_code] = True

            ess = ExamStartSignal()
            start_time = datetime.datetime.now().timetuple()
            start_time = time.mktime(start_time)

            h_a_s = HonorCodeAcceptSingal()
            h_a_s.update_honor_code_accept_Signal(
                {'useruid': request.user.id,
                 'exam_code': int(exam_code),
                 'ess_time': int(start_time)},
                {'accept': 1}
            )

            ess.insert_exam_start_signal({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'start': 1,
                'start_time': int(start_time),
                'end': 0
            })
            return HttpResponse(
                json.dumps(
                    {'status': 'ok', 'url': '/cps/' + exam_code + '/'}
                )
            )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'Not Authorized for this action'}
                )
            )

    def set_exam_finished(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code', '')
            redirect = request.POST.get('redirect', '')
            ess = ExamStartSignal()
            end_time = datetime.datetime.now().timetuple()
            end_time = time.mktime(end_time)

            validate = ess.check_exam_started({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'start': 1,
                'end': 0
            })

            h_a_s = HonorCodeAcceptSingal()
            try:
                h_a_s.update_honor_code_accept_Signal({
                    'useruid': request.user.id,
                    'exam_code': int(exam_code),
                    'ess_time': int(validate['start_time'])},
                    {'accept': 0})
            except:
                pass

            ess.update_exam_start_signal({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'start': 1},
                {'end': 1,
                 'start': 0,
                 'end_time': end_time}
            )
            request.session['current_question_number'] = ''
            if redirect == '1':
                return HttpResponse(
                    json.dumps(
                        {'status': 'ok',
                         'redirect': 1,
                         'url': '/results/' + exam_code + '/'}
                    )
                )
            else:
                return HttpResponse(
                    json.dumps(
                        {'status': 'ok', 'redirect': 0}
                    )
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'Not Authorized for this action'}
                )
            )

    def save_category(self, request):
        user = UserProfile()
        if request.user.is_authenticated():
            ioe_check = bool(request.POST.get('ioe_check', ''))
            iom_check = bool(request.POST.get('iom_check', ''))
            if ioe_check and iom_check:
                cat = 'IDP'
            elif ioe_check:
                cat = 'BE-IOE'
            elif iom_check:
                cat = 'MBBS-IOM'
            user.update_upsert(
                {'username': request.user.username},
                {'student_category': cat,
                 'student_category_set': 1}
            )
            return HttpResponse(json.dumps({'status': 'ok'}))
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'You are not authorized to perform \
                     this action.'}
                )
            )

    def get_nexp_page_of_questions(self, request):
        user_profile_obj = UserProfile()
        exam_code = int(request.POST['exam_code'])
        subscribed = user_profile_obj.check_subscribed(
            request.user.username, exam_code
        )
        if request.user.is_authenticated() and subscribed:
            user_det = user_profile_obj.get_user_by_username(
                request.user.username
            )
            parameters = {}
            parameters['user'] = user_det
            ess = ExamStartSignal()
            exam_obj = ExammodelApi()

            exam_details = exam_obj.find_one_exammodel(
                {'exam_code': int(exam_code)}
            )
            current_time = time.mktime(datetime.datetime.now().timetuple())

            validate_start = ess.check_exam_started(
                {'exam_code': int(exam_code),
                 'useruid': request.user.id,
                 'start': 1,
                 'end': 0}
            )

            if validate_start is not None:
                check = validate_start['start_time']
            else:
                ess.update_exam_start_signal({
                    'exam_code': int(exam_code),
                    'useruid': request.user.id},
                    {'start': 1,
                     'start_time': int(
                         time.mktime(datetime.datetime.now().timetuple())
                     ),
                     'end': 0,
                     'end_time': ''
                     })
                validate_start = ess.check_exam_started(
                    {'exam_code': int(exam_code),
                     'useruid': request.user.id,
                     'start': 1,
                     'end': 0}
                )
                check = validate_start['start_time']

            if current_time - check > exam_details['exam_duration'] * 60:
                ess.update_exam_start_signal({
                    'exam_code': int(exam_code),
                    'useruid': request.user.id,
                    'start': 1},
                    {'end': 1,
                     'start': 0,
                     'end_time': int(
                         time.mktime(datetime.datetime.now().timetuple())
                     )
                     })
                ess.update_exam_start_signal({
                    'exam_code': int(exam_code),
                    'useruid': request.user.id},
                    {'start': 1,
                     'start_time': int(
                         time.mktime(datetime.datetime.now().timetuple())
                     ),
                     'end': 0,
                     'end_time': ''
                     })
                validate_start = ess.check_exam_started(
                    {'exam_code': int(exam_code),
                     'useruid': request.user.id,
                     'start': 1,
                     'end': 0}
                )
                check = validate_start['start_time']

            if current_time - check < exam_details['exam_duration'] * 60:
                atte_ans = AttemptedAnswerDatabase()
                all_answers = atte_ans.find_all_atttempted_answer({
                    'exam_code': int(exam_code),
                    'user_id': int(request.user.id),
                    'ess_time': int(validate_start['start_time'])
                })
                time_elapsed = time.mktime(
                    datetime.datetime.now().timetuple()
                ) - validate_start['start_time']
                exam_details['exam_duration'] = (
                    exam_details['exam_duration'] * 60 - time_elapsed
                ) / 60

                parameters['all_answers'] = json.dumps(all_answers)
                question_obj = QuestionApi()

                current_pg_num = 1
                next_page = 0

                if request.POST.get('current', '') != '':
                    current_pg_num = int(request.POST.get('current', ''))

                if request.POST.get('next', '') != '':
                    next_page = int(request.POST.get('next', ''))

                if next_page == 1:
                    current_pg_num = current_pg_num + 1
                if next_page == -1:
                    current_pg_num = current_pg_num - 1

                if current_pg_num < 1:
                    current_pg_num = 1

                parameters['page_end'] = False
                if current_pg_num > 4:
                    current_pg_num = 5
                    parameters['page_end'] = True

                parameters['current_pg_num'] = current_pg_num
                exam_handler_obj = ExamHandler()
                questions = exam_handler_obj.get_paginated_question_set(
                    int(exam_code), current_pg_num
                )

                # print questions
                sorted_questions = sorted(
                    questions, key=lambda k: k['question_number']
                )

                # parameters['questions'] = json.dumps(sorted_questions)
                parameters['questions'] = sorted_questions
                parameters['exam_details'] = exam_details

                parameters['exam_code'] = exam_code
                user_profile_obj = UserProfile()
                user = user_profile_obj.get_user_by_username(
                    request.user.username
                )
                parameters['user'] = user
                html = str(render_to_response(
                    'ajax_exammain.html',
                    parameters,
                    context_instance=RequestContext(request))
                )
                html = html.replace(
                    'Content-Type: text/html; charset=utf-8', ''
                )
                return HttpResponse(
                    json.dumps(
                        {'status': 'ok',
                         'html': html,
                         'all_ans': all_answers,
                         'current_pg_num': current_pg_num}
                    )
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'You are not authorized to \
                     perform this action.'}
                )
            )

    def get_next_page_of_cps_exam(self, request):
        user_profile_obj = UserProfile()
        exam_code = int(request.POST['exam_code'])
        subscribed = user_profile_obj.check_subscribed(
            request.user.username, exam_code
        )
        if request.user.is_authenticated() and subscribed:
            parameters = {}
            exam_obj = ExammodelApi()
            user_profile_obj = UserProfile()
            question_obj = QuestionApi()
            ess = ExamStartSignal()
            atte_ans = AttemptedAnswerDatabase()
            # questions = question_obj.find_all_questions(
                # {"exam_code": int(exam_code)}, fields={'answer.correct':0}
            # )
            user = user_profile_obj.get_user_by_username(request.user.username)
            exam_details = exam_obj.find_one_exammodel(
                {'exam_code': int(exam_code)}
            )

            validate = ess.check_exam_started(
                {'exam_code': int(exam_code),
                 'useruid': request.user.id,
                 'start': 1,
                 'end': 0}
            )
            if validate is None:
                start_time = time.mktime(datetime.datetime.now().timetuple())
                ess.insert_exam_start_signal({
                    'exam_code': int(exam_code),
                    'useruid': request.user.id,
                    'start': 1,
                    'start_time': int(start_time),
                    'end': 0
                })

            current_time = time.mktime(datetime.datetime.now().timetuple())
            if current_time - exam_details['exam_date'] <= \
                    exam_details['exam_duration'] * 60:

                validate_start = ess.check_exam_started(
                    {'exam_code': int(exam_code),
                     'useruid': request.user.id,
                     'start': 1,
                     'end': 0}
                )
                all_answers = atte_ans.find_all_atttempted_answer({
                    'exam_code': int(exam_code),
                    'user_id': int(request.user.id),
                    'ess_time': int(validate_start['start_time'])
                })
                time_elapsed = time.mktime(
                    datetime.datetime.now().timetuple()
                ) - int(exam_details['exam_date'])

                current_pg_num = 1
                next_page = 0

                if request.POST.get('current', '') != '':
                    current_pg_num = int(request.POST.get('current', ''))

                if request.POST.get('next', '') != '':
                    next_page = int(request.POST.get('next', ''))

                if next_page == 1:
                    current_pg_num = current_pg_num + 1
                if next_page == -1:
                    current_pg_num = current_pg_num - 1

                if current_pg_num < 1:
                    current_pg_num = 1

                parameters['page_end'] = False
                if current_pg_num > 4:
                    current_pg_num = 5
                    parameters['page_end'] = True

                parameters['current_pg_num'] = current_pg_num

                exam_handler_obj = ExamHandler()
                questions = exam_handler_obj.get_paginated_question_set(
                    int(exam_code), current_pg_num
                )
                sorted_questions = sorted(
                    questions, key=lambda k: k['question_number']
                )

                parameters['all_answers'] = all_answers
                parameters['questions'] = sorted_questions
                exam_details['exam_duration'] = (
                    exam_details['exam_duration'] * 60 - time_elapsed
                ) / 60
                exam_details['exam_date'] = datetime.datetime.fromtimestamp(
                    int(exam_details['exam_date'])
                ).strftime('%Y-%m-%d')
                parameters['exam_details'] = exam_details
                parameters['exam_code'] = exam_code
                parameters['user'] = user
                html = str(render_to_response(
                    'ajax_exammain.html',
                    parameters,
                    context_instance=RequestContext(request))
                )
                html = html.replace(
                    'Content-Type: text/html; charset=utf-8', ''
                )
                return HttpResponse(json.dumps(
                    {'status': 'ok',
                     'html': html,
                     'all_ans': all_answers,
                     'current_pg_num': current_pg_num})
                )

            else:
                return HttpResponse(
                    json.dumps(
                        {'status': 'error',
                         'message': 'You are not authorized to \
                         perform this action.'}
                    )
                )

    def load_result(self, request):
        self.set_exam_finished(request)
        parameters = {}
        res = {}
        exam_code = request.POST.get('exam_code')
        res['exam_code'] = int(exam_code)
        exam_obj = ExammodelApi()
        exam_details = exam_obj.find_one_exammodel(
            {'exam_code': int(exam_code)}
        )
        res['exam_details'] = exam_details
        ess = ExamStartSignal()
        ess_check = ess.check_exam_started(
            {'exam_code': int(exam_code),
             'useruid': request.user.id}
        )

        total_questions = 65
        ans = AttemptedAnswerDatabase()
        try:
            all_ans = ans.find_all_atttempted_answer({
                'exam_code': int(exam_code),
                'user_id': request.user.id,
                'ess_time': ess_check['start_time']
            },
                fields={'q_no': 1, 'attempt_details': 1}
            )
        except:
            all_ans = ''
        answer_list = ''
        anss = []
        for eachAns in all_ans:
            anss.append(eachAns['q_no'])
        if exam_details['exam_category'] == 'BE-IOE':
            loop_start = 1
            loop_end = total_questions + 1
        else:
            loop_start = 0
            loop_end = total_questions 

        for i in range(loop_start, loop_end):
            try:
                if i in anss:
                    answer_list += all_ans[anss.index(i)][
                        'attempt_details'][0]['selected_ans']
                else:
                    answer_list += 'e'
            except:
                answer_list += 'e'

        exam_handler = ExamHandler()
        score_list = exam_handler.check_answers(exam_code, answer_list)
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user
        parameters['result'] = score_list
        from apps.mainapp.classes.result import Result
        result_obj = Result()
        result_obj.save_result(
            {
                'useruid': request.user.id,
                'exam_code': int(exam_code),
                'ess_time': ess_check['start_time'],
                'result': score_list
            }
        )
        parameters['exam_completed'] = True
        if request.user.is_authenticated():
            current_time = time.mktime(datetime.datetime.now().timetuple())
            if exam_details['exam_family'] == 'CPS' and current_time - \
                    exam_details['exam_date'] < exam_details['exam_duration'] \
                    * 60:
                parameters['exam_completed'] = False

        parameters['exam_code'] = exam_code
        parameters['myrankcard'] = {'total': 200, 'rank': 1}
        html = str(render_to_response(
                   'ajax_results.html',
                   parameters,
                   context_instance=RequestContext(request)
                   ))
        html = html.replace('Content-Type: text/html; charset=utf-8', '')
        return HttpResponse(json.dumps({'status': 'ok', 'html': html}))

    def get_unattempted_questions_number(self, request):
        exam_code = int(request.POST.get('exam_code'))
        ess = ExamStartSignal()
        validate_start = ess.check_exam_started(
            {'exam_code': int(exam_code),
             'useruid': request.user.id,
             'start': 1,
             'end': 0}
        )
        atte_ans = AttemptedAnswerDatabase()
        all_answers = atte_ans.find_all_atttempted_answer({
            'exam_code': int(exam_code),
            'user_id': int(request.user.id),
            'ess_time': int(validate_start['start_time'])
        })

        questions_list = []
        for eachAns in all_answers:
            questions_list.append(eachAns['q_no'])

        not_attempted = ''
        for i in range(1, 66):
            if i not in questions_list:
                not_attempted += str(i) + ', '

        not_attempted = not_attempted[0: (len(not_attempted) - 2)]
        cnt_att = len(all_answers)
        nt_att = 65 - cnt_att
        return HttpResponse(
            json.dumps(
                {'status': 'ok',
                 'questions': not_attempted,
                 'attempted': cnt_att,
                 'notattempted': nt_att}
            )
        )


    def get_new_exam(self, request):
        user_profile_obj = UserProfile()
        ex_type = request.POST.get('type')
        if request.user.is_authenticated():
            if ex_type == 'be-ioe':
                exam_code = generate_random_ioe_questions(request)
            else:
                exam_code = generate_random_iom_questions(request)

            user_profile_obj.save_valid_exam(
                request.user.username, int(exam_code)
            )
            return HttpResponse(
                json.dumps(
                    {'exam_code': int(exam_code), 'status': 'ok', 'type': ex_type}
                )
            )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'You are not authorized to \
                     perform this action'}
                )
            )

    def chek_valid_dps_code(self, request):
        if request.user.is_authenticated():
            user_profile_obj = UserProfile()
            coupon_obj = Coupon()
            code = request.POST.get('code')
            ex_type = request.POST.get('type')
            coupon_code = coupon_obj.get_unused_coupon_by_coupon_code(code)

            if coupon_code is None:
                return HttpResponse(
                    json.dumps(
                        {'message': 'Invalid Coupon Code.',
                         'status': 'error'}
                    )
                )

            if 'BE-IOE' in coupon_code['subscription_type']:
                user_profile_obj.change_subscription_plan(
                    request.user.username, code
                )
                coupon_obj.change_used_status_of_coupon(
                    code, request.user.username
                )
                return HttpResponse(
                    json.dumps({'message': 'valid', 'status': 'ok', 'type':ex_type})
                )

            elif 'MBBS-IOM' in coupon_code['subscription_type']:
                user_profile_obj.change_subscription_plan(
                    request.user.username, code
                )
                coupon_obj.change_used_status_of_coupon(
                    code, request.user.username
                )
                return HttpResponse(
                    json.dumps({'message': 'valid', 'status': 'ok', 'type':ex_type})
                )

            elif 'DPS' in coupon_code['subscription_type']:
                coupon_obj.change_used_status_of_coupon(
                    code, request.user.username
                )
                return HttpResponse(
                    json.dumps({'message': 'valid', 'status': 'ok', 'type':ex_type})
                )

            else:
                return HttpResponse(
                    json.dumps(
                        {'message': 'Invalid Coupon Code.', 'status': 'error'}
                    )
                )

        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'You are not authorized to \
                     perform this action'}
                )
            )
