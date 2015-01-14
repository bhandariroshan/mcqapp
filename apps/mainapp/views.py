import time
import datetime
import json
import subprocess

'''
required for pulchowkexam system

from facepy import GraphAPI

from allauth.socialaccount.models import SocialToken, SocialAccount
'''
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.facebook.views import login_by_token

from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test, login_required

from .classes.notifications import Notifications
from .classes.MailChimp import MailChimp
from .classes.Coupon import Coupon
from .classes.result import Result
from .classes.Userprofile import UserProfile
from .classes.CouponCount import CouponCount
from .classes.query_database import QuestionApi, ExammodelApi,\
    ExamStartSignal, AttemptedAnswerDatabase,\
    CurrentQuestionNumber
from .decorators import user_authenticated_and_subscribed_required

from apps.exam_api.views import ExamHandler
from apps.mainapp.classes.referral import Referral
from apps.mainapp.classes.CouponRequestEmail import CouponEmail


def new_dashboard(request):
    parameters = {}
    if request.user.is_authenticated():        
        sign_up_sign_in(request, android_user=False)
        # exam_dict = {'ioe': 'BE-IOE', 'iom': 'MBBS-IOM'}
        user_profile_obj = UserProfile()
        # exam_model_api = ExammodelApi()
        user = user_profile_obj.get_user_by_username(request.user.username)
        exam_model_api = ExammodelApi()

        # exam_dict = {'ioe': 'BE-IOE', 'iom': 'MBBS-IOM'}

        parameters['all_subscribed'] = False
        parameters['ioe_subscribed'] = False
        parameters['iom_subscribed'] = False

        if "IDP" in user['subscription_type']:
            parameters['all_subscribed'] = True

        if 'BE-IOE' in user['subscription_type']:
            parameters['ioe_subscribed'] = True

        if 'MBBS-IOM' in user['subscription_type']:
            parameters['iom_subscribed'] = True

        print parameters['all_subscribed']
        if user is None:
            raise Http404

        parameters['user'] = user
        return render_to_response(
                'newdashboard.html', parameters, context_instance=RequestContext(request)
            )
    else:        
        try:
            del request.session['ref_id']
        except:
            pass
        if request.GET.get('refid') is not None:
            request.session['ref_id'] = request.GET.get('refid')
        # ref_id = request.GET.get('refid', '')
        # parameters['ref_id'] = ref_id
        return render_to_response(
            'landing.html', parameters, context_instance=RequestContext(request)
        )


def sign_up_sign_in(request, android_user=False):
    social_account = SocialAccount.objects.get(user__id=request.user.id)
    user_profile_object = UserProfile()
    user = user_profile_object.get_user_by_username(request.user.username)
    if user is not None:
        return None

    valid_exams = []
    coupons = []
    subscription_type = []
    join_time = datetime.datetime.now()
    join_time = time.mktime(join_time.timetuple())
    student_category = 'IDP'
    student_category_set = 0

    data = {
        'useruid': int(request.user.id),
        'first_name': social_account.extra_data.get('first_name'),
        'last_name': social_account.extra_data.get('last_name'),
        'name': social_account.extra_data.get('name'),
        'username': request.user.username,
        "link": social_account.extra_data.get('link'),
        "id": social_account.extra_data.get('id'),
        "timezone": social_account.extra_data.get('timezone'),
        "email": social_account.extra_data.get('email'),
        "locale": social_account.extra_data.get('locale'),
        'coupons': coupons,
        'valid_exam': valid_exams,
        'subscription_type': subscription_type,
        'newsletter_freq': 'Weekly',
        'join_time': int(join_time),
        'student_category': student_category,
        'student_category_set': student_category_set
    }

    if android_user is True:
        data['android_user'] = True
        data['registration_id'] = request.POST.get('registration_id', '')
    else:
        data['web_user'] = True
        data['registration_id'] = ''

    mc = MailChimp()
    try:
        mc.subscribe(data)
    except:
        pass
    data['mc_subscribed'] = True
    return user_profile_object.update_upsert(
        {'username': request.user.username}, data
    )


def get_all_questions(request):
    question_api = QuestionApi()

    questions = question_api.find_all_questions(
        {"question.html": {"$exists": False}},
        fields={'question_number': 1,
                'exam_code': 1,
                'question': 1,
                'answer': 1,
                '_id': 0}
    )

    return HttpResponse(json.dumps({"status": "ok", "result": questions}))


def latex_html(request):
    return render_to_response(
        "sample-tex.html", {'exam': request.GET.get('exam')},
        context_instance=RequestContext(request)
    )


@csrf_exempt
def add_html(request):
    questions = json.loads(request.POST.get('q'))
    for question in questions:
        question_api = QuestionApi()
        question_api.latex_html(
            {"exam_code": int(question['exam_code']),
             "question_number": question['question_number']},
            {"question.html": question['question']['text'],
             "answer.a.html": question['answer']['a']['text'],
             "answer.b.html": question['answer']['b']['text'],
             "answer.c.html": question['answer']['c']['text'],
             "answer.d.html": question['answer']['d']['text']
             }
        )
    return render_to_response(
        "sample-tex.html", context_instance=RequestContext(request)
    )


@csrf_exempt
def android(request):
    login_by_token(request)
    if request.user.is_authenticated():
        sign_up_sign_in(request, android_user=True)
        return HttpResponse(json.dumps({'status': 'ok'}))
    else:
        return HttpResponse(
            json.dumps(
                {'status': 'error', 'message': 'User not authenticated'}
            )
        )


def androidapk(request):
    return HttpResponseRedirect(
        'https://play.google.com/store/apps/details?id=com.meroanswer'
    )
    # return HttpResponseRedirect('http://bit.ly/meroanswer')


def set_category(request):
    parameters = {}
    if request.user.is_authenticated():
        sign_up_sign_in(request, android_user=False)
        ref_id = request.session.get('ref_id')

        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)

        if 'MBBS-IOM' in user['student_category']:
            return HttpResponseRedirect('/iom/')

        elif 'BE-IOE' in user['student_category']:
            return HttpResponseRedirect('/ioe/')

        # new user so add to referral
        if ref_id is not None:
            ref_obj = Referral()
            user_id = request.user.id
            if ref_obj.check_referral_storage(user_id) is None:
                ref_id = ref_obj.update_invite_accept_list(ref_id, user_id)
        parameters['user'] = user
        return render_to_response(
            'setcategory.html', parameters,
            context_instance=RequestContext(request)
        )
    else:
        try:
            del request.session['ref_id']
        except:
            pass
        if request.GET.get('refid') is not None:
            request.session['ref_id'] = request.GET.get('refid')
        # ref_id = request.GET.get('refid', '')
        # parameters['ref_id'] = ref_id
        return render_to_response(
            'landing.html', parameters, context_instance=RequestContext(request)
        )


@login_required
def user_dashboard(request, exam_type):
    parameters = {}
    exam_dict = {'ioe': 'BE-IOE', 'iom': 'MBBS-IOM'}
    user_profile_obj = UserProfile()
    exam_model_api = ExammodelApi()
    user = user_profile_obj.get_user_by_username(request.user.username)

    # get or set user referral id
    ref_obj = Referral()
    user_id = request.user.id
    myref_obj = ref_obj.get_referral_id(user_id)
    parameters['ref_id'] = myref_obj['uid']['id']
    parameters['ref_count'] = len(myref_obj['invite_acceptuids'])

    if user is None:
        raise Http404

    parameters['user'] = user
    parameters['exam_type'] = exam_type

    parameters['subscribed'] = True
    if "IDP" in user['subscription_type']:
        parameters['all_subscribed'] = True
    elif exam_dict[exam_type] in user['subscription_type']:
        parameters[str(exam_type) + '_subscribed'] = True
    else:
        parameters['subscribed'] = False

    all_dps_exams = exam_model_api.find_all_exammodel_descending(
        {'exam_code': {'$in': user['valid_exam']},
         'exam_family': 'DPS',
         'exam_category': exam_dict[exam_type]},
        sort_index='exam_date'
    )
    parameters['all_dps_exams'] = all_dps_exams

    cps_exams = exam_model_api.find_all_exammodel_descending(
        {'exam_family': 'CPS',
         'exam_category': exam_dict[exam_type]},
        sort_index='exam_date'
    )
    all_cps_exams = []
    for cps_exams in cps_exams:
        up_cps_exam = {}
        up_cps_exam['exam_subscribed'] = True
        if not parameters['subscribed']:
            up_cps_exam['exam_subscribed'] = cps_exams.get('exam_code') in user['valid_exam']

        up_cps_exam['exam_details'] = cps_exams
        all_cps_exams.append(up_cps_exam)

    parameters['all_cps_exams'] = all_cps_exams

    return render_to_response(
        'dashboard.html',
        parameters,
        context_instance=RequestContext(request)
    )


@user_authenticated_and_subscribed_required
def attend_cps_exam(request, exam_code):
    parameters = {}
    user_profile_obj = UserProfile()
    ess = ExamStartSignal()
    exam_obj = ExammodelApi()

    user = user_profile_obj.get_user_by_username(request.user.username)

    if user is None:
        raise Http404

    exam_details = exam_obj.find_one_exammodel(
        {'exam_code': int(exam_code)}
    )

    if exam_details is None:
        raise Http404

    current_time = time.mktime(datetime.datetime.now().timetuple())

    if current_time < exam_details['exam_date']:
        return HttpResponseRedirect('/')

    # exm_date_time_linux = exam_details['exam_date']

    if_cps_ended = ess.check_exam_started(
        {'exam_code': int(exam_code),
         'useruid': request.user.id, 'start': 0, 'end': 1}
    )
    if if_cps_ended is not None:
        return HttpResponseRedirect('/results/' + str(exam_code) + '/')

    validate = ess.check_exam_started(
        {'exam_code': int(exam_code),
         'useruid': request.user.id, 'start': 1, 'end': 0}
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

    if current_time - exam_details['exam_date'] > exam_details['exam_duration'] * 60:
        return HttpResponseRedirect('/results/' + str(exam_code))

    validate_start = ess.check_exam_started(
        {'exam_code': int(exam_code), 'useruid': request.user.id,
         'start': 1, 'end': 0}
    )
    atte_ans = AttemptedAnswerDatabase()
    all_answers = atte_ans.find_all_atttempted_answer({
        'exam_code': int(exam_code), 'user_id': int(request.user.id),
        'ess_time': int(validate_start['start_time'])
    })
    time_elapsed = current_time - int(exam_details['exam_date'])
    exam_handler_obj = ExamHandler()

    '''
    The code below is needed for pulchowkexam system

    # current_pg_num = 1
    # next_page = 0

    # if request.GET.get('current', '') != '':
    #     current_pg_num = int(request.POST.get('current', ''))

    # if request.GET.get('next', '') != '':
    #     next_page = int(request.GET.get('next', ''))

    # if next_page == 1:
    #     current_pg_num = current_pg_num + 1

    # if next_page == -1:
    #     current_pg_num = current_pg_num - 1

    # if current_pg_num < 1:
    #     current_pg_num = 1

    # parameters['page_end'] = False
    # if current_pg_num > 4:
    #     current_pg_num = 5
    #     parameters['page_end'] = True

    # parameters['current_pg_num'] = current_pg_num

    # exam_handler_obj.get_paginated_question_set(
    #     int(exam_code), current_pg_num
    # )
    '''

    exam_handler_obj.get_questionset_from_database(
        int(exam_code), False
    )
    questions = exam_handler_obj.sorted_question_list

    for count, eachQuestion in enumerate(questions):
        eachQuestion['question_number'] = count + 1
    parameters['max_questions_number'] = len(questions)

    start_question_number = 0
    cqn = CurrentQuestionNumber()
    current_q_no = cqn.check_current_question_number({
        'exam_code': int(exam_code),
        'useruid': request.user.id,
        'ess_time': int(validate_start['start_time'])
    })
    try:
        start_question_number = current_q_no['cqn']
        if start_question_number == '':
            start_question_number = 0
    except:
        start_question_number = 0

    if start_question_number == len(questions):
        start_question_number = start_question_number - 1
        parameters['next_to_start'] = questions[start_question_number]
    else:
        parameters['next_to_start'] = questions[0]
    parameters['start_question_number'] = start_question_number
    parameters['start_question'] = questions[start_question_number]

    parameters['all_answers'] = json.dumps(all_answers)
    parameters['questions'] = json.dumps(questions)
    exam_details['exam_duration'] = (exam_details['exam_duration'] * 60 - time_elapsed) / 60
    parameters['exam_details'] = exam_details
    parameters['user'] = user

    '''
    The code below is needed for pulchowkexam system

    # if exm_date_time_linux <= time.mktime(datetime.datetime.now().timetuple()):
    #     parameters['render_before_exam'] = False
    # else:
    #     parameters['render_before_exam'] = True
    # return render_to_response(
    #     'pulchowkexam-main.html', parameters,
    #     context_instance=RequestContext(request)
    # )
    '''

    return render_to_response(
        'exam_main.html',
        parameters,
        context_instance=RequestContext(request)
    )


@user_authenticated_and_subscribed_required
def attend_dps_exam(request, exam_code):
    user_profile_obj = UserProfile()
    user_det = user_profile_obj.get_user_by_username(request.user.username)

    if user_det is None:
        raise Http404

    parameters = {}
    parameters['user'] = user_det
    ess = ExamStartSignal()

    '''

    This code is required for pulchowkexam system

    try:
        profile_image = user_det['profile_image']
    except:
        social_account = SocialAccount.objects.get(
            user__id=request.user.id
        )
        access_token = SocialToken.objects.get(
            account__user__id=request.user.id
        )

        graph = GraphAPI(access_token)
        det = graph.get(
            social_account.uid +
            '/picture/?redirect=0&height=300&type=normal&width=300'
        )
        profile_image = det['data']['url']
        user_profile_obj.update_profile_image(
            profile_image, request.user.username
        )
    '''

    exam_obj = ExammodelApi()
    exam_details = exam_obj.find_one_exammodel(
        {'exam_code': int(exam_code)}
    )

    if exam_details is None:
        raise Http404

    current_time = time.mktime(datetime.datetime.now().timetuple())

    validate_start = ess.check_exam_started(
        {'exam_code': int(exam_code), 'useruid': request.user.id,
         'start': 1, 'end': 0}
    )

    if validate_start is not None:
        check = validate_start['start_time']
    else:
        ess.update_exam_start_signal({
            'exam_code': int(exam_code),
            'useruid': request.user.id}, {
            'start': 1,
            'start_time': int(current_time),
            'end': 0,
            'end_time': ''
        })

        check = current_time

    if current_time - check > exam_details['exam_duration'] * 60:
        ess.update_exam_start_signal({
            'exam_code': int(exam_code),
            'useruid': request.user.id,
            'start': 1},
            {
                'end': 1, 'start': 0,
                'end_time': int(current_time)
            }
        )
        ess.update_exam_start_signal({
            'exam_code': int(exam_code),
            'useruid': request.user.id},
            {
                'start': 1,
                'start_time': int(current_time),
                'end': 0,
                'end_time': ''
            })

        check = current_time

    if current_time - check < exam_details['exam_duration'] * 60:
        atte_ans = AttemptedAnswerDatabase()
        all_answers = atte_ans.find_all_atttempted_answer({
            'exam_code': int(exam_code), 'user_id': int(request.user.id),
            'ess_time': int(check)
        })
        time_elapsed = current_time - check
        exam_details['exam_duration'] = (
            exam_details['exam_duration'] * 60 - time_elapsed) / 60

        parameters['all_answers'] = json.dumps(all_answers)

        exam_handler_obj = ExamHandler()

        '''
        This code is required= for pulchowkexam system

        current_pg_num = 1
        next_page = 0

        if request.GET.get('current', '') != '':
            current_pg_num = int(request.GET.get('current', ''))

        if request.GET.get('next', '') != '':
            next_page = int(request.GET.get('next', ''))

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
        exam_handler_obj.get_paginated_question_set(
            int(exam_code), current_pg_num
        )

        '''

        exam_handler_obj.get_questionset_from_database(
            int(exam_code), False
        )
        questions = exam_handler_obj.sorted_question_list
        for count, eachQuestion in enumerate(questions):
            eachQuestion['question_number'] = count + 1

        start_question_number = 0
        cqn = CurrentQuestionNumber()
        current_q_no = cqn.check_current_question_number({
            'exam_code': int(exam_code),
            'useruid': request.user.id,
            'ess_time': check
        })
        try:
            start_question_number = current_q_no['cqn']
            if start_question_number == '':
                start_question_number = 0
        except:
            start_question_number = 0

        if start_question_number == len(questions):
            start_question_number = start_question_number - 1
            parameters['next_to_start'] = questions[start_question_number]
        else:
            parameters['next_to_start'] = questions[0]
        parameters['start_question_number'] = start_question_number
        parameters['start_question'] = questions[start_question_number]

        parameters['questions'] = json.dumps(questions)
        parameters['exam_details'] = exam_details

        parameters['max_questions_number'] = len(exam_details['question_list'])

        return render_to_response(
            'exam_main.html',
            parameters,
            context_instance=RequestContext(request)
        )

        # return render_to_response(
        #     'pulchowkexam-main.html',
        #     parameters,
        #     context_instance=RequestContext(request)
        # )

@csrf_exempt
def subscription(request):
    parameters = {}
    user_profile_obj = UserProfile()
    if request.method == 'POST':
        formtype = request.POST.get('formtype')
        if formtype == None:
            email = request.POST.get('email')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            parameters ['name_error'],  parameters['phone_error'], parameters['email_error'] = False, False, False

            if email == '':
                parameters['email_error'] = True
                parameters['email_error_message'] = 'Please enter a valid email.'
            if len(phone) < 6:
                parameters['phone_error'] = True
                parameters['phone_error_message'] = 'Please enter a valid phone.'

            if len(name) < 3:
                parameters['name_error'] = True
                parameters['name_error_message'] = 'Please enter a valid name.'

            if parameters['name_error'] or parameters['email_error'] or parameters['phone_error']:
                parameters['success'] = False
            else:
                parameters['success'] = True

            email_obj = CouponEmail()
            email_obj.send_coupon_requested_email(request, name, phone, email)

        else:
            coupon_obj = Coupon()
            coupon_code = request.POST.get('coupon', '')
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)

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
                coupon_obj.change_used_status_of_coupon(
                    coupon_code, request.user.username
                )
                parameters['coupon_message'] = 'Congratulations, you have sussessfully subscribed.'
                parameters['coupon_message_true'] = True
            else:
                pass
                

    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    parameters['is_user_subscribed'] = False
    if user !=None:
        if 'BE-IOE' in user['subscription_type'] or 'MBBS-IOM' in user['subscription_type']:
            parameters['is_user_subscribed'] = True
        
        
    return render_to_response(
            'subscription.html', 
            parameters, 
            context_instance=RequestContext(request)
        )



def tos(request):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    return render_to_response(
        'tos.html',
        parameters,
        context_instance=RequestContext(request)
    )


def request_coupon(request):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    return render_to_response(
        'coupon_contact.html',
        parameters,
        context_instance=RequestContext(request)
    )


def privacy(request):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    return render_to_response(
        'privacy.html',
        parameters,
        context_instance=RequestContext(request)
    )

@csrf_exempt
def distributors(request):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        parameters ['name_error'],  parameters['phone_error'], parameters['email_error'] = False, False, False

        if email == '':
            parameters['email_error'] = True
            parameters['email_error_message'] = 'Please enter a valid email.'
        if len(phone) < 6:
            parameters['phone_error'] = True
            parameters['phone_error_message'] = 'Please enter a valid phone.'

        if len(name) < 3:
            parameters['name_error'] = True
            parameters['name_error_message'] = 'Please enter a valid name.'

        if parameters['name_error'] or parameters['email_error'] or parameters['phone_error']:
            parameters['success'] = False
        else:
            parameters['success'] = True

        email_obj = CouponEmail()
        email_obj.send_coupon_requested_email(request, name, phone, email)
    return render_to_response(
        'distributors.html',
        parameters,
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def generate_coupon(request, subscription_type):
    # 1. DPS (Daily Practice Set)
    # 2. CPS (Competitive Pracice Set)
    # 3. MBBS-IOM
    # 4. BE-IOE
    # 5. IDP (Inter Disciplinary Plan)
    coupon = Coupon()
    if subscription_type == 'beioe':
        subscription_type = 'BE-IOE'
    elif subscription_type == 'mbbsiom':
        subscription_type = 'MBBS-IOM'
    coupon.update_coupons(subscription_type.upper())
    coupon.generate_coupons(subscription_type.upper())
    return HttpResponse(
        json.dumps(
            {'status': 'success',
             'message': subscription_type + ' coupons generated'}
        )
    )


@user_passes_test(lambda u: u.is_superuser)
def get_coupons(request, subscription_type):
    coupon_obj = Coupon()
    coupon_count = CouponCount()
    base_count = coupon_count.get_coupon_count()
    if base_count is not None:
        base_count = base_count['count']
    else:
        base_count = 1000
    if subscription_type == 'beioe':
        subscription_type = 'BE-IOE'
    elif subscription_type == 'mbbsiom':
        subscription_type = 'MBBS-IOM'
    subscription_type = subscription_type.upper()
    coupons = coupon_obj.get_coupons(subscription_type)
    page_obj = Paginator(coupons, 12)
    for i in range(1, page_obj.num_pages + 1):
        count = base_count + (i - 1) * 12
        for cc, each_coup in enumerate(page_obj.page(i)):
            coupon_obj.update_serial_no(
                serial_no=int(count + cc + 1), coupon_code=each_coup['code']
            )
        abc = render_to_response(
            'coupons-print.html',
            {'coupons': page_obj.page(i), 'count': count}
        )
        Html_file = open(
            settings.APP_ROOT + "/../meroanswer-coupons/htmls/" +
            "coupon-" + str(i) + ".html", "w"
        )
        Html_file.write(str(abc))
        Html_file.close()

    coupon_count.update_coupon_count(count)
    subprocess.call(['../meroanswer-coupons/coupon-gen.sh'])
    return HttpResponse(
        json.dumps(
            {'status': 'ok',
             'message': str(page_obj.num_pages) + ' Page ' +
             subscription_type + ' coupons generated'}
        )
    )


@login_required
def results(request, exam_code):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    exam_obj = ExammodelApi()
    exam_details = exam_obj.find_one_exammodel({'exam_code': int(exam_code)})

    if exam_details is None:
        raise Http404

    ess = ExamStartSignal()
    ess_check = ess.check_exam_started(
        {'exam_code': int(exam_code),
         'useruid': request.user.id}
    )

    parameters['exam_completed'] = True
    current_time = time.mktime(datetime.datetime.now().timetuple())
    if exam_details['exam_family'] == 'CPS' and current_time - exam_details['exam_date'] < exam_details['exam_duration'] * 60:
        parameters['exam_completed'] = False

    result_obj = Result()
    user_result = result_obj.find_all_result(
        {'exam_code': int(exam_code),
         'useruid': request.user.id,
         'ess_time': ess_check['start_time']}
    )
    if len(user_result) > 0:
        score_list = []
        for results in user_result:
            score_list.append(results['result'])
    else:
        exam_handler = ExamHandler()
        exam_handler.save_exam_result(
            request, exam_details, ess_check['start_time']
        )
        score_list = exam_handler.user_exam_result
    parameters['result'] = score_list
    parameters['exam_code'] = exam_code
    parameters['myrankcard'] = {'total': 200, 'rank': 1}
    return render_to_response(
        'results.html',
        parameters,
        context_instance=RequestContext(request)
    )


def notifications(request):
    if request.user.is_authenticated():
        notices = Notifications()
        return HttpResponse(
            json.dumps(
                {'status': 'ok',
                 'result': notices.get_notifications(request.user.id)}
            )
        )
    else:
        return HttpResponse(json.dumps(
            {'status': 'error',
             'message': 'You are not authorized to perform this action.'})
        )


@user_authenticated_and_subscribed_required
def show_result(request, exam_code, subject_name):
    exam_obj = ExammodelApi()
    exam_handler_obj = ExamHandler()
    exam_details = exam_obj.find_one_exammodel(
        {'exam_code': int(exam_code)}
    )

    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    
    if exam_details is None:
        raise Http404

    current_time = time.mktime(datetime.datetime.now().timetuple())
    if exam_details['exam_family'] == 'CPS' and current_time - exam_details['exam_date'] < exam_details['exam_duration'] * 60:
        return HttpResponseRedirect('/')

    exam_handler_obj.get_filtered_question_from_database(
        int(exam_code), subject_name
    )
    questions = exam_handler_obj.sorted_question_list
    total_questions = len(questions)
    try:
        current_q_no = int(request.GET.get('q', ''))
        if current_q_no >= total_questions:
            current_q_no = next_q_no = total_questions - 1
        else:
            next_q_no = current_q_no + 1
        if current_q_no <= 0:
            current_q_no = previous_q_no = 0
        else:
            previous_q_no = current_q_no - 1
    except:
        current_q_no = 0
        previous_q_no = 0
        next_q_no = 1

    parameters['current_q_no'] = current_q_no

    parameters['question_number'] = questions[
        current_q_no]['question_number']
    parameters['question'] = questions[current_q_no]
    parameters['subject'] = subject_name
    parameters['exam_code'] = exam_code
    parameters['next_q_no'] = next_q_no
    parameters['previous_q_no'] = previous_q_no

    ess = ExamStartSignal()
    ans = AttemptedAnswerDatabase()
    ess_check = ess.check_exam_started(
        {'exam_code': int(exam_code),
         'useruid': request.user.id}
    )

    try:
        query = {'exam_code': int(exam_code),
                 'user_id': int(request.user.id),
                 'ess_time': ess_check['start_time'],
                 'q_id': questions[current_q_no]['uid']['id']}
        att_ans = ans.find_all_atttempted_answer(query)
        parameters['attempted'] = att_ans[0]['attempt_details'][-1]['selected_ans']
    except:
        parameters['attempted'] = ''
    return render_to_response(
        'single-result.html',
        parameters,
        context_instance=RequestContext(request)
    )


def get_list_of_result(request):
    if request.user.is_authenticated():
        exam_obj = ExammodelApi()
        result_obj = Result()
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        return_dict = []
        for exam_code in user['valid_exam']:
            exam_details = exam_obj.find_one_exammodel(
                {'exam_code': int(exam_code)}
            )
            if exam_details is None or exam_details['exam_family'] == 'DPS':
                continue
            user_result = result_obj.find_all_result(
                {'exam_code': int(exam_code),
                 'useruid': request.user.id}
            )
            score_list = []
            for results in user_result:
                score_list.append(results['result'])
            return_dict.append(
                {'exam_code': int(exam_code),
                 'ess_time': user_result[0]['ess_time'],
                 'result': score_list,
                 'exam_details': exam_details,
                 'rank': 0}
            )
        return HttpResponse(json.dumps(
            {'status': 'ok', 'result': return_dict})
        )
    else:
        return HttpResponse(json.dumps(
            {'status': 'error', 'message': 'Not a valid request'})
        )


def androidurl(request):
    return HttpResponseRedirect('http://bit.ly/meroanswer')


def couponpage(request):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    return render_to_response(
        'coupon.html',
        parameters,
        context_instance=RequestContext(request)
    )


def couponspage_redirect(request):
    return HttpResponseRedirect('/coupon/')


def subject_history(request, subject_name):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)

    parameters['user'] = user
    return render_to_response(
        'history.html',
        parameters,
        context_instance=RequestContext(request)
    )    

def history(request):
    parameters = {}
    user_profile_obj = UserProfile()
    
    user = user_profile_obj.get_user_by_username(request.user.username)
    exam_history = user_profile_obj.get_exams_history_for_user(request.user.username)
    parameters['exam_history'] = exam_history

    parameters['user'] = user
    return render_to_response(
        'history.html',
        parameters,
        context_instance=RequestContext(request)
    ) 
       
def add_chapters(request):
    parameters = {}
    user_profile_obj = UserProfile()    
    user = user_profile_obj.get_user_by_username(request.user.username)

    from apps.mainapp.classes.Questions import Question
    questions_obj = Question()
    parameters['questions'] = questions_obj.get_questions(request.user.username)

    # for subject in ['physics', 'chemistry', 'mathematics', 'english', 'zoology', 'botany']:

        
    parameters['user'] = user
    return render_to_response(
        'chapters.html',
        parameters,
        context_instance=RequestContext(request)
    )    