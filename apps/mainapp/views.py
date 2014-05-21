from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.mainapp.classes.Exams import Exam, RankCard, ScoreCard
from apps.mainapp.classes.Schedules  import Schedules
import time, datetime
from django.http import HttpResponse
from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
import json
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.models import User
from django.contrib.auth import authenticate # Does not give me access
# For POSTing the facebook token
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.socialaccount.helpers import complete_social_login

from django import forms
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken, SocialAccount
from allauth.socialaccount.providers.facebook.views import login_by_token
from allauth.socialaccount.models import SocialToken, SocialAccount


def latex_html(request): 
    return render_to_response("sample-tex.html")

@csrf_exempt
def add_html(request): 
    print request.POST.get('q')
    questions = json.loads(request.POST.get('q'))

    for question in questions:
        question_api = QuestionApi()
        question_api.latex_html({"exam_code":int(question['exam_code']), \
            "question_number":question['question_number']}, \
             {"question.html":question['question']['text'], \
             "answer.a.html":question['answer']['a']['text'],
             "answer.b.html":question['answer']['b']['text'],
             "answer.c.html":question['answer']['c']['text'],
             "answer.d.html":question['answer']['d']['text']\
             })
    return render_to_response("sample-tex.html")

@csrf_exempt
def android(request): 
    login_by_token(request)
    if request.user.is_authenticated():
        social_account = SocialAccount.objects.get(user__id=request.user.id)
        from apps.mainapp.classes.Userprofile import UserProfile
        user_profile_object = UserProfile()
        user = user_profile_object.get_user_by_username(request.user.username)
        try:
            valid_exams = user['valid_exam']
            if 'IOM-SAMPLE-1' not in valid_exams:
                valid_exams.append('IOM-SAMPLE-1')
            if 'IOE-SAMPLE-1' not in valid_exams:
                valid_exams.append('IOE-SAMPLE-1')
            if 'IOE-SAMPLE-2' not in valid_exams:
                valid_exams.append('IOE-SAMPLE-2')
            if 'IOM-SAMPLE-2' not in valid_exams:
                valid_exams.append('IOM-SAMPLE-2')
        except:
            valid_exams=['IOM-SAMPLE-1', 'IOE-SAMPLE-1','IOM-SAMPLE-2','IOE-SAMPLE-2']

        try:
            coupons = user['coupons']
        except:
            coupons = []
        try:
            subscription_type = user['subscription_type']
        except:
            subscription_type = []
        try:
            join_time = user['join_time']
        except:
            join_time = datetime.datetime.now()
            join_time = time.mktime(join_time.timetuple())

        data = {
                'useruid': int(request.user.id), 
                'first_name': social_account.extra_data['first_name'],
                'last_name': social_account.extra_data['last_name'],
                'name':social_account.extra_data['name'],
                'username' : request.user.username,
                "link": social_account.extra_data['link'],
                "id": social_account.extra_data['id'],
                "timezone": social_account.extra_data['timezone'],
                "email": social_account.extra_data['email'],
                "locale": social_account.extra_data['locale'],
                'coupons':coupons,
                'valid_exam':valid_exams,
                'subscription_type':subscription_type,
                'newsletter_freq':'Weekly',
                'android_user':True,
                'join_time':int(join_time)
        }
        try:
            mc_subscribed = user['subscribed_to_mailchimp']            
        except:
            from apps.mainapp.classes.MailChimp import MailChimp
            mc = MailChimp()
            mc.subscribe(data)
            mc_subscribed = True
        data['mc_subscribed'] = mc_subscribed        

        user_profile_object.update_upsert({'username':request.user.username}, data)
        return HttpResponse(json.dumps({'status':'ok'}))
    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'User not authenticated'}))


def dashboard(request):
    if request.user.is_authenticated():
        social_account = SocialAccount.objects.get(user__id=request.user.id)
        from apps.mainapp.classes.Userprofile import UserProfile        
        user_profile_object = UserProfile()
        user = user_profile_object.get_user_by_username(request.user.username)
        try:
            valid_exams = user['valid_exam']
            if 'IOM-SAMPLE-1' not in valid_exams:
                valid_exams.append('IOM-SAMPLE-1')
            if 'IOE-SAMPLE-1' not in valid_exams:
                valid_exams.append('IOE-SAMPLE-1')
            if 'IOE-SAMPLE-2' not in valid_exams:
                valid_exams.append('IOE-SAMPLE-2')
            if 'IOM-SAMPLE-2' not in valid_exams:
                valid_exams.append('IOM-SAMPLE-2')
        except:
            valid_exams=['IOM-SAMPLE-1', 'IOE-SAMPLE-1','IOM-SAMPLE-2','IOE-SAMPLE-2']

        try:
            coupons = user['coupons']
        except:
            coupons = []
        try:
            subscription_type = user['subscription_type']
        except:
            subscription_type = []
        try:
            join_time = user['join_time']
        except:
            join_time = datetime.datetime.now()
            join_time = time.mktime(join_time.timetuple())
        data = {
                'useruid': int(request.user.id), 
                'first_name': social_account.extra_data['first_name'],
                'last_name': social_account.extra_data['last_name'],
                'name':social_account.extra_data['name'],
                'username' : request.user.username,
                 "link": social_account.extra_data['link'],
                 "id": social_account.extra_data['id'],
                 "timezone": social_account.extra_data['timezone'],
                 "email": social_account.extra_data['email'],
                "locale": social_account.extra_data['locale'],
                'coupons':coupons,
                'valid_exam':valid_exams,
                'subscription_type':subscription_type,
                'newsletter_freq':'Weekly',
                'join_time':int(join_time)
        }
        
        try:
            mc_subscribed = user['subscribed_to_mailchimp']            
        except:
            from apps.mainapp.classes.MailChimp import MailChimp
            mc = MailChimp()
            mc.subscribe(data)
            mc_subscribed = True
        data['mc_subscribed'] = mc_subscribed 

        user_profile_object.update_upsert({'username':request.user.username}, data)
        return HttpResponseRedirect('/')

    else:
        return HttpResponseRedirect('/')

def landing(request):
    if request.user.is_authenticated():
        exam_obj = Exam()
        upcoming_exams = exam_obj.get_upcoming_exams()
        parameters = {}        
        up_exams = []
        print upcoming_exams
        for eachExam in upcoming_exams:
            up_exm = {}
            up_exm['name'] = eachExam['exam_name']
            up_exm['code'] = eachExam['exam_code']
            up_exm['exam_time'] = eachExam['exam_time']
            up_exm['exam_category'] = eachExam['exam_category']
            up_exm['image'] = eachExam['image']
            up_exm['exam_date'] = datetime.datetime.fromtimestamp(int(eachExam['exam_date'])).strftime("%A, %d. %B %Y")
            up_exams.append(up_exm)
        parameters['upcoming_exams'] = up_exams

        schedule_obj = Schedules()
        schedules = schedule_obj.get_upcoming_schedules()
        up_schedules = []
        for eachSchedule in schedules:
            up_sch = {}
            up_sch['name'] = eachSchedule['name']
            up_sch['code'] = eachSchedule['code']
            up_sch['schedule_time'] = eachSchedule['schedule_time']
            up_sch['schedule_category'] = eachSchedule['schedule_category']
            up_sch['image'] = eachSchedule['image']
            up_sch['schedule_date'] = datetime.datetime.fromtimestamp(int(eachSchedule['schedule_date'])).strftime("%A, %d. %B %Y")
            up_schedules.append(up_sch)
        parameters['upcoming_schedules'] = up_schedules

        rank_card_obj = RankCard()
        rank_card = rank_card_obj.get_rank_card(request.user.id, 'IOMMBBSMODEL000')
        try:
            parameters['rank_card'] = rank_card[0]
        except:
            pass

        score_card_obj = ScoreCard()        
        socre_card = score_card_obj.get_score_card(request.user.id, 'IOMMBBSMODEL000')
        try:
            parameters['socre_card'] = socre_card[0]        
        except:
            pass

        return render_to_response('dashboard.html',parameters,
                              context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def attempt_question(request):
    return render_to_response('qone-one.html',context_instance=RequestContext(request))


def landing(request):
    if request.user.is_authenticated():
        exam_obj = Exam()
        upcoming_exams = exam_obj.get_upcoming_exams()
        parameters = {}        
        up_exams = []

        user_profile_obj = UserProfile()
        subscribed_exams = user_profile_obj.get_subscribed_exams(request.user.username)
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user

        subscription_type = user['subscription_type']
        for eachExam in upcoming_exams:            
            up_exm = {}
            
            up_exm['name'] = eachExam['exam_name']
            
            if 'IDP' in subscription_type:
                up_exm['subscribed'] = True

            elif eachExam['exam_category'] in subscription_type:
                up_exm['subscribed'] = True

            else:
                up_exm['subscribed'] = eachExam['exam_code'] in subscribed_exams

            up_exm['code'] = eachExam['exam_code']
            up_exm['exam_time'] = eachExam['exam_time']
            up_exm['exam_category'] = eachExam['exam_category']
            up_exm['image'] = eachExam['image']
            up_exm['exam_date'] = datetime.datetime.fromtimestamp(int(eachExam['exam_date'])).strftime("%A, %d. %B %Y")
            up_exams.append(up_exm)

        parameters['upcoming_exams'] = up_exams
        # print up_exams

        schedule_obj = Schedules()
        schedules = schedule_obj.get_upcoming_schedules()
        up_schedules = []
        for eachSchedule in schedules:
            up_sch = {}
            up_sch['name'] = eachSchedule['name']
            up_sch['code'] = eachSchedule['code']
            up_sch['schedule_time'] = eachSchedule['schedule_time']
            up_sch['schedule_category'] = eachSchedule['schedule_category']
            up_sch['image'] = eachSchedule['image']
            up_sch['schedule_date'] = datetime.datetime.fromtimestamp(int(eachSchedule['schedule_date'])).strftime("%A, %d. %B %Y")
            up_schedules.append(up_sch)
        parameters['upcoming_schedules'] = up_schedules

        rank_card_obj = RankCard()
        rank_card = rank_card_obj.get_rank_card(request.user.id, 'IOMMBBSMODEL000')
        try:
            parameters['rank_card'] = rank_card[0]
        except:
            pass

        score_card_obj = ScoreCard()        
        socre_card = score_card_obj.get_score_card(request.user.id, 'IOMMBBSMODEL000')
        try:
            parameters['socre_card'] = socre_card[0]        
        except:
            pass

        return render_to_response('dashboard.html',parameters,
                              context_instance=RequestContext(request))
    else:
        return render_to_response('landing.html', context_instance=RequestContext(request))

def attend_exam(request,exam_code):
    if exam_code == '100':
        subscribed = True
    else:
        coupon_obj = Coupon()    
        subscribed = coupon_obj.check_subscried(exam_code, request.user.id)
    if request.user.is_authenticated() and subscribed:
        question_obj = QuestionApi()    
        questions = question_obj.find_all_questions({"exam_code": int(exam_code)})
        sorted_questions = sorted(questions, key=lambda k: k['question_number'])

        exam_obj = ExammodelApi()
        exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})
        exam_details['exam_date'] = datetime.datetime.fromtimestamp(int(exam_details['exam_date'])).strftime('%Y-%m-%d')


        parameters = {}
        parameters['questions'] = json.dumps(sorted_questions)
        parameters['exam_details'] = exam_details
    
        start_question_number = 0 
        parameters['start_question'] = sorted_questions[start_question_number]
        parameters['start_question_number'] = start_question_number
        parameters['max_questions_number'] =  len(sorted_questions)

        parameters['exam_code'] = exam_code
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user
        return render_to_response('exam_main.html', parameters, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def honorcode(request, exam_code):
    user_profile_obj = UserProfile()
    subscribed = user_profile_obj.check_subscribed(request.user.username, exam_code)
    if request.user.is_authenticated() and subscribed:
        exam_obj = ExammodelApi()
        exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})
        exam_details['exam_date'] = datetime.datetime.fromtimestamp(int(exam_details['exam_date'])).strftime('%Y-%m-%d')

        parameters = {}
        parameters['exam_details'] = exam_details
        parameters['exam_code'] = exam_code
        
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user

        return render_to_response('exam_tips_and_honor_code.html', parameters, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def subscription(request):
    parameters = {}    
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    return render_to_response('subscription.html', parameters, context_instance=RequestContext(request))
