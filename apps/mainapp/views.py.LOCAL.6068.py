import time
import datetime
import json
from facepy import GraphAPI

from allauth.socialaccount.models import SocialToken, SocialAccount
from allauth.socialaccount.providers.facebook.views import login_by_token

from django.http import Http404

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test

from apps.mainapp.classes.notifications import Notifications
from apps.mainapp.classes.MailChimp import MailChimp
from apps.mainapp.classes.Exams import RankCard, ScoreCard
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
from apps.exam_api.views import ExamHandler
from bson.objectid import ObjectId
from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi,\
    ExamStartSignal, HonorCodeAcceptSingal, AttemptedAnswerDatabase,\
    CurrentQuestionNumber


def sign_up_sign_in(request, android_user=False):
    social_account = SocialAccount.objects.get(user__id=request.user.id)
    access_token = SocialToken.objects.get(account__user__id=request.user.id)
    user_profile_object = UserProfile()
    user = user_profile_object.get_user_by_username(request.user.username)
    if user != None:
        return None

    valid_exams = []
    coupons = []    
    subscription_type = []
    join_time = datetime.datetime.now()
    join_time = time.mktime(join_time.timetuple())
    graph = GraphAPI(access_token)
    det = graph.get(social_account.uid + '/picture/?redirect=0&height=300&type=normal&width=300')
    profile_image = det['data']['url']
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
        data['android_user'] = False
        data['registration_id'] = ''

    mc = MailChimp()
    try:
        mc.subscribe(data)
    except:
        pass
    data['mc_subscribed'] = True
    return user_profile_object.update_upsert({'username': request.user.username}, data)


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
    return render_to_response("sample-tex.html", context_instance=RequestContext(request))


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


def dashboard(request):
    if request.user.is_authenticated():
        sign_up_sign_in(request, android_user=False)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def landing(request):
    if request.user.is_authenticated():
        parameters = {}
        up_exams = []

        user_profile_obj = UserProfile()
        subscribed_exams = user_profile_obj.get_subscribed_exams(
            request.user.username
        )
        user = user_profile_obj.get_user_by_username(request.user.username)
        exam_handler = ExamHandler()
        exam_model_api = ExammodelApi()
        user_exams = user['valid_exam']

        parameters['user'] = user
        subscription_type = user['subscription_type']

        if len(subscription_type) != 0:
            parameters['subscribed'] = True
        else:
            parameters['subscribed'] = False

        parameters['subscription_type'] = user['subscription_type']
        
        try:
            if user['student_category_set'] == 1:
                parameters['student_category_set'] = True
            else:
                parameters['student_category_set'] = False
        except:
            parameters['student_category_set'] = False

        for eachExam in user_exams:
            up_exm = {}
            eaxhExamDetails = exam_model_api.find_one_exammodel({'exam_code':eachExam})
            up_exm['name'] = eaxhExamDetails['exam_name']

            if 'IDP' in subscription_type:
                up_exm['subscribed'] = True

            elif eaxhExamDetails['exam_category'] in subscription_type:
                up_exm['subscribed'] = True

            else:
                up_exm['subscribed'] = eaxhExamDetails['exam_code'] in \
                    subscribed_exams

            up_exm['code'] = eaxhExamDetails['exam_code']
            if eaxhExamDetails['exam_family'] != 'DPS':
                exam_start_time = datetime.datetime.strptime(
                    str(datetime.datetime.fromtimestamp(
                        int(eaxhExamDetails['exam_date']))),
                    "%Y-%m-%d %H:%M:%S").time()
                up_exm['exam_time'] = exam_start_time
                up_exm['exam_date'] = datetime.datetime.fromtimestamp(
                    int(eaxhExamDetails['exam_date'])
                ).strftime("%A, %d. %B %Y")
            up_exm['exam_category'] = eaxhExamDetails['exam_category']
            up_exm['exam_family'] = eaxhExamDetails['exam_family']
            up_exm['image'] = eaxhExamDetails['image']
            up_exams.append(up_exm)

        parameters['upcoming_exams'] = up_exams

        rank_card_obj = RankCard()
        rank_card = rank_card_obj.get_rank_card(
            request.user.id, 'IOMMBBSMODEL000'
        )
        try:
            parameters['rank_card'] = rank_card[0]
        except:
            pass

        score_card_obj = ScoreCard()
        socre_card = score_card_obj.get_score_card(
            request.user.id, 'IOMMBBSMODEL000'
        )
        try:
            parameters['socre_card'] = socre_card[0]
        except:
            pass
        parameters['has_result'] = False
        return render_to_response(
            'dashboard.html', parameters,
            context_instance=RequestContext(request)
        )
    else:
        return render_to_response(
            'landing.html', context_instance=RequestContext(request)
        )


def attend_cps_exam(request, exam_code):
    user_profile_obj = UserProfile()
    subscribed = user_profile_obj.check_subscribed(
        request.user.username, exam_code
    )
    if request.user.is_authenticated() and subscribed:
        parameters = {}
        ess = ExamStartSignal()
        exam_obj = ExammodelApi()
        user_profile_obj = UserProfile()
        question_obj = QuestionApi()
        ess = ExamStartSignal()
        atte_ans = AttemptedAnswerDatabase()
        # questions = question_obj.find_all_questions(
            # {"exam_code": int(exam_code)}, fields={'answer.correct':0})
        user = user_profile_obj.get_user_by_username(request.user.username)
        exam_details = exam_obj.find_one_exammodel(
            {'exam_code': int(exam_code)}
        )
        exm_date_time_linux = exam_details['exam_date']

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

        current_time = time.mktime(datetime.datetime.now().timetuple())
        if current_time - exam_details['exam_date'] > \
                exam_details['exam_duration'] * 60:
            # print "Redirected to results"
            return HttpResponseRedirect('/results/' + str(exam_code))

        validate_start = ess.check_exam_started(
            {'exam_code': int(exam_code), 'useruid': request.user.id,
             'start': 1, 'end': 0}
        )
        all_answers = atte_ans.find_all_atttempted_answer({
            'exam_code': int(exam_code), 'user_id': int(request.user.id),
            'ess_time': int(validate_start['start_time'])
        })
        time_elapsed = time.mktime(datetime.datetime.now().timetuple()) - \
            int(exam_details['exam_date'])
        total_questions = question_obj.get_count(
            {"exam_code": int(exam_code), 'marks': 1}
        )
        current_pg_num = 1
        next_page = 0

        if request.GET.get('current', '') != '':
            current_pg_num = int(request.POST.get('current', ''))

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

        questions = question_obj.get_paginated_questions(
            {"exam_code": int(exam_code), 'marks': 1},
            fields={'answer.correct': 0}, page_num=current_pg_num
        )
        sorted_questions = sorted(
            questions, key=lambda k: k['question_number']
        )

        parameters['all_answers'] = json.dumps(all_answers)
        parameters['questions'] = sorted_questions
        exam_details['exam_duration'] = (exam_details['exam_duration'] * 60 -
                                         time_elapsed) / 60
        exam_details['exam_date'] = datetime.datetime.fromtimestamp(
            int(exam_details['exam_date'])
        ).strftime('%Y-%m-%d')
        parameters['exam_details'] = exam_details
        parameters['max_questions_number'] = total_questions
        parameters['exam_code'] = exam_code
        parameters['user'] = user
        if exm_date_time_linux <= time.mktime(
                datetime.datetime.now().timetuple()):
            parameters['render_before_exam'] = False
        else:
            parameters['render_before_exam'] = True
        return render_to_response(
            'pulchowkexam-main.html', parameters,
            context_instance=RequestContext(request)
        )

    else:
        return HttpResponseRedirect('/')


def attend_dps_exam(request, exam_code):
    user_profile_obj = UserProfile()
    subscribed = user_profile_obj.check_subscribed(
        request.user.username, exam_code
    )
    if request.user.is_authenticated() and subscribed:
        user_det = user_profile_obj.get_user_by_username(request.user.username)
        parameters = {}
        parameters['user'] = user_det
        ess = ExamStartSignal()
        exam_obj = ExammodelApi()
        exam_handler_obj = ExamHandler()
        ess = ExamStartSignal()

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

        exam_details = exam_obj.find_one_exammodel(
            {'exam_code': int(exam_code)}
        )
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
                'start_time': int(
                    time.mktime(datetime.datetime.now().timetuple())),
                'end': 0,
                'end_time': ''
            })
            validate_start = ess.check_exam_started(
                {'exam_code': int(exam_code),
                 'useruid': request.user.id,
                 'start': 1, 'end': 0}
            )
            check = validate_start['start_time']

        if current_time - check > exam_details['exam_duration'] * 60:
            ess.update_exam_start_signal({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'start': 1},
                {
                    'end': 1, 'start': 0,
                    'end_time': int(
                        time.mktime(datetime.datetime.now().timetuple())
                    )
                }
            )
            ess.update_exam_start_signal({
                'exam_code': int(exam_code),
                'useruid': request.user.id},
                {
                    'start': 1,
                    'start_time': int(
                        time.mktime(datetime.datetime.now().timetuple())
                    ),
                    'end': 0,
                    'end_time': ''
                })
            validate_start = ess.check_exam_started(
                {'exam_code': int(exam_code),
                 'useruid': request.user.id,
                 'start': 1, 'end': 0}
            )
            check = validate_start['start_time']

        if current_time - check < exam_details['exam_duration'] * 60:
            atte_ans = AttemptedAnswerDatabase()
            all_answers = atte_ans.find_all_atttempted_answer({
                'exam_code': int(exam_code), 'user_id': int(request.user.id),
                'ess_time': int(validate_start['start_time'])})
            time_elapsed = time.mktime(
                datetime.datetime.now().timetuple()) - validate_start[
                'start_time']
            exam_details['exam_duration'] = (
                exam_details['exam_duration'] * 60 - time_elapsed) / 60

            parameters['all_answers'] = json.dumps(all_answers)


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
            questions = exam_handler_obj.get_paginated_question_set(
                int(exam_code), current_pg_num
            )

            sorted_questions = sorted(
                questions, key=lambda k: k['question_number']
            )
            parameters['questions'] = sorted_questions
            parameters['exam_details'] = exam_details

            parameters['max_questions_number'] = 65

            parameters['exam_code'] = exam_code
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            parameters['user'] = user
            return render_to_response(
                'pulchowkexam-main.html',
                parameters,
                context_instance=RequestContext(request)
            )

    else:
        return HttpResponseRedirect('/')


def attend_dps_exam_old(request, exam_code):
    user_profile_obj = UserProfile()
    subscribed = user_profile_obj.check_subscribed(
        request.user.username, exam_code
    )
    if request.user.is_authenticated() and subscribed:
        parameters = {}
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
                'useruid': request.user.id}, {
                'start': 1,
                'start_time': int(
                    time.mktime(datetime.datetime.now().timetuple())),
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
                {
                    'end': 1,
                    'start': 0,
                    'end_time': int(
                        time.mktime(datetime.datetime.now().timetuple()))})
            ess.update_exam_start_signal({
                'exam_code': int(exam_code),
                'useruid': request.user.id},
                {
                    'start': 1,
                    'start_time': int(
                        time.mktime(datetime.datetime.now().timetuple())),
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
                'ess_time': int(validate_start['start_time'])})
            time_elapsed = time.mktime(datetime.datetime.now().timetuple()) -\
                validate_start['start_time']
            exam_details['exam_duration'] = (
                exam_details['exam_duration'] * 60 - time_elapsed
            ) / 60

            parameters['all_answers'] = json.dumps(all_answers)
            question_obj = QuestionApi()
            questions = question_obj.find_all_questions(
                {"exam_code": int(exam_code),
                 'marks': 1},
                fields={'answer.correct': 0}
            )
            total_questions = question_obj.get_count(
                {"exam_code": int(exam_code), 'marks': 1}
            )
            sorted_questions = sorted(
                questions, key=lambda k: k['question_number']
            )

            parameters['questions'] = json.dumps(sorted_questions)
            parameters['exam_details'] = exam_details

            start_question_number = 0
            cqn = CurrentQuestionNumber()
            current_q_no = cqn.check_current_question_number({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'ess_time': validate_start['start_time']
            })
            try:
                start_question_number = current_q_no['cqn']
                if start_question_number == '':
                    start_question_number = 0
            except:
                start_question_number = 0

            if start_question_number == total_questions:
                start_question_number = start_question_number - 1
                parameters['next_to_start'] = sorted_questions[
                    start_question_number]
            else:
                parameters['next_to_start'] = sorted_questions[0]

            parameters['start_question_number'] = start_question_number
            parameters['start_question'] = sorted_questions[
                start_question_number]
            parameters['max_questions_number'] = total_questions

            parameters['exam_code'] = exam_code
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            parameters['user'] = user
            return render_to_response(
                'exam_main.html',
                parameters,
                context_instance=RequestContext(request)
            )

    else:
        return HttpResponseRedirect('/')


def honorcode(request, exam_code):
    parameters = {}
    exam_obj = ExammodelApi()
    user_profile_obj = UserProfile()
    h_a_s = HonorCodeAcceptSingal()
    ess = ExamStartSignal()
    user = user_profile_obj.get_user_by_username(request.user.username)
    exam_details = exam_obj.find_one_exammodel(
        {'exam_code': int(exam_code)}
    )
    subscribed = user_profile_obj.check_subscribed(
        request.user.username, exam_code
    )
    current_time = time.mktime(datetime.datetime.now().timetuple())

    if request.user.is_authenticated() and subscribed:
        if exam_details['exam_family'] == 'DPS':
            return HttpResponseRedirect('/dps/' + str(exam_code) + '/')

        current_time = time.mktime(datetime.datetime.now().timetuple())
        if current_time - exam_details['exam_date'] > \
                exam_details['exam_duration'] * 60:
            return HttpResponseRedirect('/results/' + str(exam_code))

        if_cps_ended = ess.check_exam_started(
            {'exam_code': int(exam_code),
             'useruid': request.user.id,
             'start': 0,
             'end': 1}
        )
        if if_cps_ended is not None:
            return HttpResponseRedirect('/results/' + str(exam_code) + '/')

        elif exam_details['exam_family'] == 'CPS':
            if current_time < exam_details['exam_date']:
                parameters['render_before_exam'] = True

            elif current_time > exam_details['exam_date']:
                parameters['render_before_exam'] = False

        exam_details['exam_date'] = datetime.datetime.fromtimestamp(
            int(exam_details['exam_date'])
        )
        validate_start = ess.check_exam_started(
            {'exam_code': int(exam_code),
             'useruid': request.user.id,
             'start': 1}
        )
        if validate_start is not None:
            h_a_s_accepted = h_a_s.check_honor_code_accepted({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'accept': 1,
                'ess_time': validate_start['start_time']
            })
        else:
            h_a_s_accepted = None

        if h_a_s_accepted is None:
            parameters['exam_code'] = exam_code
            parameters['user'] = user
            parameters['exam_details'] = exam_details

            return render_to_response(
                'exam_tips_and_honor_code.html',
                parameters,
                context_instance=RequestContext(request)
            )
        else:
            return HttpResponseRedirect('/cps/' + str(exam_code) + '/')
    else:
        return HttpResponseRedirect('/')


def subscription(request):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
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


def distributors(request):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    return render_to_response(
        'distributors.html',
        parameters,
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def generate_coupon(request):
    # 1. DPS (Daily Practice Set)
    # 2. CPS (Competitive Pracice Set)
    # 3. MBBS-IOM
    # 4. BE-IOE
    # 5. IDP (Inter Disciplinary Plan)
    coupon = Coupon()
    # # coupon.generate_coupons('IDP')
    coupon.generate_coupons('DPS')
    # coupon.generate_coupons('CPS')
    # coupon.generate_coupons('BE-IOE')
    # coupon.generate_coupons('MBBS-IOM')
    return HttpResponse(json.dumps({'status': 'success'}))


@user_passes_test(lambda u: u.is_superuser)
def get_coupons(request, subscription_type):
    coupon_obj = Coupon()
    if subscription_type == 'beioe':
        subscription_type = 'BE-IOE'
    elif subscription_type == 'mbbsiom':
        subscription_type = 'MBBS-IOM'
    subscription_type = subscription_type.upper()
    coupons = coupon_obj.get_coupons(subscription_type)
    # coupon_obj.update_coupons(subscription_type)
    return HttpResponse(json.dumps({'status': 'ok', 'coupons': coupons}))


def results(request, exam_code):
    parameters = {}
    res = {}
    res['exam_code'] = int(exam_code)
    exam_obj = ExammodelApi()
    exam_details = exam_obj.find_one_exammodel({'exam_code': int(exam_code)})
    res['exam_details'] = exam_details
    ess = ExamStartSignal()
    ess_check = ess.check_exam_started(
        {'exam_code': int(exam_code),
         'useruid': request.user.id}
    )

    question_obj = QuestionApi()
    total_questions = question_obj.get_count(
        {"exam_code": int(exam_code), 'marks': 1}
    )

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
    for i in range(1, total_questions + 1):
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
    result_obj.save_result({
            'useruid':request.user.id, 
            'exam_code':int(exam_code), 
            'ess_time':ess_check['start_time'], 
            'result':score_list
            })
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


def show_result(request, exam_code, subject_name):
    user_profile_obj = UserProfile()
    exam_obj = ExammodelApi()
    subscribed = user_profile_obj.check_subscribed(
        request.user.username, exam_code
    )
    exam_details = exam_obj.find_one_exammodel(
        {'exam_code': int(exam_code)}
    )
    parameters = {}
    if request.user.is_authenticated() and subscribed:
        current_time = time.mktime(datetime.datetime.now().timetuple())
        if exam_details['exam_family'] == 'CPS' and current_time - \
                exam_details['exam_date'] < exam_details['exam_duration'] * 60:
            return HttpResponseRedirect('/')
        parameters['exam_details'] = exam_details
        question_obj = QuestionApi()
        questions = question_obj.find_all_questions(
            {"exam_code": int(exam_code),
             'subject': str(subject_name),
             'marks': 1}
        )
        total_questions = question_obj.get_count(
            {"exam_code": int(exam_code),
             'subject': subject_name, 'marks': 1}
        )

        try:
            current_q_no = int(request.GET.get('q', ''))
            if current_q_no >= total_questions:
                next_q_no = total_questions - 1
            else:
                next_q_no = current_q_no + 1
            if current_q_no <= 0:
                previous_q_no = 0
            else:
                previous_q_no = current_q_no - 1
        except:
            current_q_no = 0
            previous_q_no = 0
            next_q_no = 1

        if current_q_no >= total_questions:
            current_q_no = total_questions - 1
        if current_q_no <= 0:
            current_q_no = 0
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
        total_questions = question_obj.get_count({"exam_code": int(exam_code)})

        try:
            query = {'exam_code': int(exam_code),
                     'user_id': int(request.user.id),
                     'ess_time': ess_check['start_time'],
                     'q_no': questions[current_q_no]['question_number']}
            att_ans = ans.find_all_atttempted_answer(query)
            parameters['attempted'] = att_ans[0]['attempt_details'][
                len(att_ans[0]['attempt_details']) - 1]['selected_ans']
        except:
            att_ans = ''
            parameters['attempted'] = ''

        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user
        return render_to_response(
            'single-result.html',
            parameters,
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect('/')


def get_list_of_result(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        ans = AttemptedAnswerDatabase()
        exam_attempts = ans.get_attempted_exams(
            'exam_code', {'user_id': request.user.id}
        )
        return_dict = []
        for exam_code in exam_attempts['results']:
            exam_obj = ExammodelApi()
            exam_details = exam_obj.find_one_exammodel(
                {'exam_code': int(exam_code)}
            )
            if exam_details['exam_family'] == 'DPS':
                continue
            attempt_timestamps = ans.get_attempted_exams(
                'ess_time',
                {'user_id': request.user.id,
                 'exam_code': int(exam_code)}
            )
            for eachAttempt in attempt_timestamps['results']:
                all_ans = ans.find_all_atttempted_answer({
                    'exam_code': int(exam_code),
                    'user_id': user_id,
                    'ess_time': eachAttempt
                })
                answer_list = ''
                anss = []
                for eachAns in all_ans:
                    anss.append(eachAns['q_no'])
                question_obj = QuestionApi()
                total_questions = question_obj.get_count(
                    {"exam_code": int(exam_code)}
                )
                for i in range(0, total_questions):
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
                rank = 0
                return_dict.append(
                    {'exam_code': exam_code,
                     'ess_time': eachAttempt,
                     'result': score_list,
                     'exam_details': exam_details,
                     'rank': rank}
                )
        return HttpResponse(json.dumps(
            {'status': 'ok', 'result': return_dict})
        )
    else:
        return HttpResponse(
            json.dumps(
                {'status': 'error',
                 'message': 'You are not authorized to perform this action.'}
            )
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


def iomdashboard(request):
    if request.user.is_authenticated():
        from apps.exam_api.views import ExamHandler
        exam_handler = ExamHandler()
        upcoming_exams = exam_handler.list_upcoming_exams(
            {'exam_category': 'MBBS-IOM'}
        )
        parameters = {}
        up_exams = []

        user_profile_obj = UserProfile()
        subscribed_exams = user_profile_obj.get_subscribed_exams(
            request.user.username
        )
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user

        subscription_type = user['subscription_type']

        if len(subscription_type) != 0:
            parameters['subscribed'] = True
        else:
            parameters['subscribed'] = False
        try:
            if user['student_category_set'] == 1:
                parameters['student_category_set'] = True
            else:
                parameters['student_category_set'] = False
        except:
            parameters['student_category_set'] = False

        for eachExam in upcoming_exams:
            up_exm = {}

            up_exm['name'] = eachExam['exam_name']

            if 'IDP' in subscription_type:
                up_exm['subscribed'] = True

            elif eachExam['exam_category'] in subscription_type:
                up_exm['subscribed'] = True

            else:
                up_exm['subscribed'] = eachExam['exam_code'] in \
                    subscribed_exams

            up_exm['code'] = eachExam['exam_code']
            if eachExam['exam_family'] != 'DPS':
                exam_start_time = datetime.datetime.strptime(
                    str(datetime.datetime.fromtimestamp(
                        int(eachExam['exam_date']
                            ))), "%Y-%m-%d %H:%M:%S").time()
                up_exm['exam_time'] = exam_start_time
                up_exm['exam_date'] = datetime.datetime.fromtimestamp(
                    int(eachExam['exam_date'])
                ).strftime("%A, %d. %B %Y")
            up_exm['exam_category'] = eachExam['exam_category']
            up_exm['exam_family'] = eachExam['exam_family']
            up_exm['image'] = eachExam['image']
            up_exams.append(up_exm)

        parameters['upcoming_exams'] = up_exams
        # print up_exams

        # schedule_obj = Schedules()
        # schedules = schedule_obj.get_upcoming_schedules()
        # up_schedules = []
        # for eachSchedule in schedules:
        #     up_sch = {}
        #     up_sch['name'] = eachSchedule['name']
        #     up_sch['code'] = eachSchedule['code']
        #     up_sch['schedule_time'] = eachSchedule['schedule_time']
        #     up_sch['schedule_category'] = eachSchedule['schedule_category']
        #     up_sch['image'] = eachSchedule['image']
        #     up_sch['schedule_date'] = datetime.datetime.fromtimestamp(
            # int(eachSchedule['schedule_date'])).strftime("%A, %d. %B %Y")
        #     up_schedules.append(up_sch)
        # parameters['upcoming_schedules'] = up_schedules

        rank_card_obj = RankCard()
        rank_card = rank_card_obj.get_rank_card(
            request.user.id, 'IOMMBBSMODEL000'
        )
        try:
            parameters['rank_card'] = rank_card[0]
        except:
            pass

        score_card_obj = ScoreCard()
        socre_card = score_card_obj.get_score_card(
            request.user.id, 'IOMMBBSMODEL000'
        )
        try:
            parameters['socre_card'] = socre_card[0]
        except:
            pass
        parameters['has_result'] = False
        return render_to_response(
            'dashboard.html',
            parameters,
            context_instance=RequestContext(request)
        )
    else:
        return render_to_response(
            'landing.html',
            context_instance=RequestContext(request)
        )


def attend_IOM_dps_exam(request, exam_code):
    user_profile_obj = UserProfile()
    subscribed = user_profile_obj.check_subscribed(
        request.user.username, exam_code
    )
    if request.user.is_authenticated() and subscribed:
        parameters = {}
        ess = ExamStartSignal()
        exam_obj = ExammodelApi()
        ess = ExamStartSignal()

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
                'useruid': request.user.id}, {
                'start': 1,
                'start_time': int(time.mktime(
                    datetime.datetime.now().timetuple())
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

        dps_exam_start = exam_details['exam_family'] == 'DPS' and current_time\
            - check > exam_details['exam_duration'] * 60
        if current_time - check > exam_details['exam_duration'] * 60:
            ess.update_exam_start_signal({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'start': 1},
                {'end': 1, 'start': 0,
                 'end_time': int(
                     time.mktime(datetime.datetime.now().timetuple()))})
            ess.update_exam_start_signal({
                'exam_code': int(exam_code),
                'useruid': request.user.id}, {
                'start': 1,
                'start_time': int(time.mktime(
                    datetime.datetime.now().timetuple())),
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
                'ess_time': int(validate_start['start_time'])})
            time_elapsed = time.mktime(datetime.datetime.now().timetuple()) -\
                validate_start['start_time']
            exam_details['exam_duration'] = (
                exam_details['exam_duration'] * 60 - time_elapsed
            ) / 60

            parameters['all_answers'] = json.dumps(all_answers)
            question_obj = QuestionApi()
            questions = question_obj.find_all_questions(
                {"exam_code": int(exam_code),
                 'marks': 1},
                fields={'answer.correct': 0}
            )
            total_questions = question_obj.get_count(
                {"exam_code": int(exam_code),
                 'marks': 1}
            )
            sorted_questions = sorted(
                questions, key=lambda k: k['question_number']
            )

            parameters['questions'] = json.dumps(sorted_questions)
            parameters['exam_details'] = exam_details

            start_question_number = 0
            cqn = CurrentQuestionNumber()
            current_q_no = cqn.check_current_question_number({
                'exam_code': int(exam_code),
                'useruid': request.user.id,
                'ess_time': validate_start['start_time']
            })
            try:
                start_question_number = current_q_no['cqn']
                if start_question_number == '':
                    start_question_number = 0
            except:
                start_question_number = 0

            if start_question_number == total_questions:
                start_question_number = start_question_number - 1
                parameters['next_to_start'] = sorted_questions[
                    start_question_number
                ]
            else:
                parameters['next_to_start'] = sorted_questions[0]

            parameters['start_question_number'] = start_question_number
            parameters['start_question'] = sorted_questions[
                start_question_number
            ]
            parameters['max_questions_number'] = total_questions

            parameters['exam_code'] = exam_code
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            parameters['user'] = user
            return render_to_response(
                'exam_main.html',
                parameters,
                context_instance=RequestContext(request)
            )

    else:
        return HttpResponseRedirect('/iom/')