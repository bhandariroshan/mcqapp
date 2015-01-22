import json
import datetime
import time

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from apps.random_questions.views import generate_random_ioe_questions, generate_random_iom_questions
from apps.random_questions.views import generate_random_moe_questions
from apps.exam_api.views import ExamHandler, save_user_answers

from .Coupon import Coupon
from .Userprofile import UserProfile
from .Exams import Exam
from .query_database import ExammodelApi, ExamStartSignal, AttemptedAnswerDatabase,\
    CurrentQuestionNumber


ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


class AjaxHandle():
    """doc string for AjaxHandle"""

    def __init__(self):
        pass

    # def get_invite_ref_id(self, request):
    #     if request.user.is_authenticated():
    #         from apps.mainapp.classes.referral import Referral
    #         ref_obj = Referral()
    #         user_id = request.user.id
    #         ref_id = ref_obj.get_referral_id(user_id)
    #         return HttpResponse(json.dumps({'status': 'ok', 'ref_id': ref_id}))
    #     else:
    #         return HttpResponse(json.dumps(
    #             {'status': 'error', 'message': 'You are not authorized to perform this action.'}
    #         ))

    def get_units(self, request):
        if request.user.is_authenticated():
            from apps.mainapp.classes.Questions import TopicApi
            topic_obj = TopicApi()
            
            subject = request.POST.get('subject','')
            uid = request.POST.get('uid','')

            units_unfiltered = topic_obj.get_topic({'subject':subject})
            units_list = []
            for eachUnits in units_unfiltered:
                if eachUnits['subject'] == subject:
                    if eachUnits['unit'] not in units_list and eachUnits['unit']!="":
                        units_list.append(eachUnits['unit'])
            return HttpResponse(json.dumps({
                        'status':'ok',
                        'subject':subject,
                        'units':units_list, 
                        'uid':uid
                    }))
        else:
            return HttpResponse({'status':'error', 'message':'Not authorized'})

    def get_chapters(self, request):
        if request.user.is_authenticated():
            from apps.mainapp.classes.Questions import TopicApi
            topic_obj = TopicApi()
            subject = request.POST.get('subject','')
            unit = request.POST.get('unit','')
            uid = request.POST.get('uid','')
            chapters_unfiltered = topic_obj.get_topic({'subject':subject, 'unit':unit})

            chapters_list = []
            for eachChapter in chapters_unfiltered:
                if eachChapter['subject'] == subject:
                    if eachChapter['chapter'] not in chapters_list and len(eachChapter['chapter']) != 0:
                        chapters_list.append(eachChapter['chapter'])
            return HttpResponse(json.dumps({
                        'status':'ok',
                        'subject':subject,
                        'unit':unit,
                        'chapters':chapters_list,
                        'uid':uid
                    }))
        else:
            return HttpResponse({'status':'error', 'message':'Not authorized'})

    def update_question(self, request):
        if request.user.is_authenticated():
            from apps.mainapp.classes.Questions import Question
            ques_obj = Question()

            from bson.objectid import ObjectId
            uid = ObjectId(str(request.POST.get('uid','')))
            subject = request.POST.get('subject','')
            unit = request.POST.get('unit','')
            chapter = request.POST.get('chapter','')
            topic = request.POST.get('topic','')
            difficulty = request.POST.get('difficulty','')
            hint = request.POST.get('hint','')
            passage_group = request.POST.get('passage_group','')
            is_passage_head = request.POST.get('is_passage_head','')

            correct = request.POST.get('correct','')
            question = request.POST.get('question','')
            opt_a = request.POST.get('opt_a','')
            opt_b = request.POST.get('opt_b','')
            opt_c = request.POST.get('opt_c','')
            opt_d = request.POST.get('opt_d','')
            # print correct, opt_a, opt_b, opt_c, opt_d, question

            if is_passage_head == 0:
                is_passage_head = False
            else:
                is_passage_head = True

            dirty_flag = False
            if subject == "Select Subject" or unit == "Select Unit" \
                or chapter == "Select chapter" or topic == "Select Topic":
                dirty_flag = True

            if subject == 'english':
                dirty_flag = False
                if passage_group !='':
                    update_data = {
                        'is_passage':True, 
                        'is_passage_head':is_passage_head,
                        'passage_group':passage_group
                    }
                else:
                    update_data = {
                        'is_passage':False, 
                        'is_passage_head':is_passage_head,
                        'passage_group':passage_group
                    }
            else:
                update_data = {
                        'flag_chapter_set':1,
                        'subject':subject, 
                        'unit':unit, 
                        'chapter':chapter, 
                        'topic':topic, 
                        'difficulty':difficulty, 
                        'hint':hint,
                        'question.text':question, 
                        'answer.a.text':opt_a, 
                        'answer.b.text':opt_b, 
                        'answer.c.text':opt_c, 
                        'answer.d.text':opt_d,
                        'answer.correct':correct
                    }
                
                for key, value in update_data.iteritems():
                    if value == "" and key != "hint":
                        dirty_flag = True

            if dirty_flag:
                return HttpResponse(json.dumps({'status':'error', 'message':'Question update error!'}))

            ques_obj.update_question({'_id':uid}, update_data)
            return HttpResponse(json.dumps({'status':'ok', 'uid':request.POST.get('uid','')}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not authorized'}))        

    def get_topics(self, request):
        if request.user.is_authenticated():
            from apps.mainapp.classes.Questions import TopicApi
            topic_obj = TopicApi()
            subject = request.POST.get('subject','')
            unit = request.POST.get('unit','')
            chapter = request.POST.get('chapter','')
            uid = request.POST.get('uid','')
            topics_unfiltered = topic_obj.get_topic({'subject':subject, 'unit':unit, 'chapter':chapter})
            topics_list = []
            for eachTopic in topics_unfiltered:
                if eachTopic['subject'] == subject and eachTopic['chapter'] == chapter and eachTopic['unit']==unit:
                    if eachTopic['topic'] not in topics_list and eachTopic['topic']!="":
                        topics_list.append(eachTopic['topic'])
            return HttpResponse(json.dumps({
                        'status':'ok',
                        'subject':subject,
                        'unit':unit,
                        'chapter':chapter,
                        'topics':topics_list,
                        'uid':uid
                    }))
        else:
            return HttpResponse({'status':'error', 'message':'Not authorized'})                
        
    def get_questions(self, request):
        if request.user.is_authenticated():
            user_profile_obj = UserProfile()
            exam_code = request.POST.get('exam_code')

            subscribed = user_profile_obj.check_subscribed(
                request.user.username, exam_code
            )

            if subscribed:
                exam_handler_obj = ExamHandler()
                exam_handler_obj.get_questionset_from_database(
                    int(exam_code), False
                )
                questions = exam_handler_obj.sorted_question_list
                for count, eachQuestion in enumerate(questions):
                    eachQuestion['question_number'] = count + 1

                return HttpResponse(json.dumps(
                    {'questions': questions, 'status': 'ok'}
                ))
            else:
                return HttpResponse(json.dumps(
                    {'status': 'error', 'message': 'You are not authorized to perform this action.'}
                ))
        else:
            return HttpResponse(json.dumps(
                {'status': 'error', 'message': 'You are not authorized to perform this action.'}
            ))

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

            if coupon_obj.validate_coupon(coupon_code, up_exm['exam_category'], up_exm['exam_family']) is True:
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
                     'message': 'Not a valid request'}
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
                     'message': 'Not a valid request'}
                )
            )

    def save_answer(self, request):
        if request.user.is_authenticated():
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
                     'message': 'Not a valid request'}
                )
            )

    def set_exam_finished(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code', '')
            redirect = request.POST.get('redirect', '')
            ess = ExamStartSignal()
            end_time = datetime.datetime.now().timetuple()
            end_time = time.mktime(end_time)

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
                     'message': 'Not a valid request'}
                )
            )

    def save_category(self, request):
        if request.user.is_authenticated():
            user = UserProfile()
            ioe_check = request.POST.get('ioe_check')
            iom_check = request.POST.get('iom_check')

            if ioe_check == 'true':
                cat = 'BE-IOE'
                url = '/ioe/'

            elif iom_check == 'true':
                cat = 'MBBS-IOM'
                url = '/iom/'
            user.update_upsert(
                {'username': request.user.username},
                {'student_category': cat,
                 'student_category_set': 1}
            )
            return HttpResponse(json.dumps({'status': 'ok', 'url': url}))

        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'Not a valid request'}
                )
            )

    def get_next_page_of_questions(self, request):
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
                exam_handler_obj.get_paginated_question_set(
                    int(exam_code), current_pg_num
                )
                questions = exam_handler_obj.sorted_question_list
                sorted_questions = sorted(
                    questions, key=lambda k: k['question_number']
                )

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
            ess = ExamStartSignal()
            atte_ans = AttemptedAnswerDatabase()
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
        if request.user.is_authenticated():
            user_profile_obj = UserProfile()
            
            ex_type = request.POST.get('type')
            # if ex_type == 'be-ioe':
            #     exam_code = generate_random_ioe_questions(request)
            # elif ex_type == 'mbbs-iom':
            #     exam_code = generate_random_iom_questions(request)
            # # elif ex_type == 'mbbs-moe':
            # #     exam_code = generate_random_moe_questions(request)


            # user_profile_obj.save_valid_exam(
            #     request.user.username, int(exam_code)
            # )
            generete_exam_response = user_profile_obj.check_generate_and_save_valid_exam(
                ex_type, request.user.username, request
            )
            
            if generete_exam_response['status'] == 'ok':
                return HttpResponse(
                    json.dumps(
                        {'exam_code': int(generete_exam_response['exam_code']), 'status': 'ok', 'type': ex_type}
                    )
                )
            else:
                return HttpResponse(
                    json.dumps(
                        {'message': generete_exam_response['message'], 'status': 'error'}
                    )
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': 'error',
                     'message': 'Not a valid request'}
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
                    json.dumps({'message': 'valid', 'status': 'ok', 'type': ex_type})
                )

            elif 'MBBS-IOM' in coupon_code['subscription_type']:
                user_profile_obj.change_subscription_plan(
                    request.user.username, code
                )
                coupon_obj.change_used_status_of_coupon(
                    code, request.user.username
                )
                return HttpResponse(
                    json.dumps({'message': 'valid', 'status': 'ok', 'type': ex_type})
                )

            elif 'DPS' in coupon_code['subscription_type']:
                coupon_obj.change_used_status_of_coupon(
                    code, request.user.username
                )
                return HttpResponse(
                    json.dumps({'message': 'valid', 'status': 'ok', 'type': ex_type})
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
                     'message': 'Not a valid request'}
                )
            )