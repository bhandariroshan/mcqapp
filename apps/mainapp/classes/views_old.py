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
from apps.mainapp.classes.query_database import ExamStartSignal
from apps.mainapp.classes.query_database import AttemptedAnswerDatabase


def sign_up_sign_in(request, android_user=False):
    social_account = SocialAccount.objects.get(user__id=request.user.id)
    from apps.mainapp.classes.Userprofile import UserProfile        
    user_profile_object = UserProfile()
    user = user_profile_object.get_user_by_username(request.user.username)
    try:
        valid_exams = user['valid_exam']
    except:
        # valid_exams=[100, 101]
        valid_exams=[]

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

    try:
        student_category = user['student_category']
    except:
        student_category = 'both'
    try:
        student_category_set = user['student_category_set']
    except:
        student_category_set = 0

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
            'join_time':int(join_time),
            'student_category':student_category,
            'student_category_set':student_category_set
    }

    if android_user == True:
        data['android_user'] = True
    else:
        data['android_user'] = False
    try:
        mc_subscribed = user['subscribed_to_mailchimp']            
    except:
        from apps.mainapp.classes.MailChimp import MailChimp
        mc = MailChimp()
        mc.subscribe(data)
        mc_subscribed = True
    data['mc_subscribed'] = mc_subscribed 
    return user_profile_object.update_upsert({'username':request.user.username}, data)

def latex_html(request): 

    return render_to_response("sample-tex.html",{'exam':request.GET.get('exam')})

@csrf_exempt
def add_html(request): 
    
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
        sign_up_sign_in(request, android_user=True)
        return HttpResponse(json.dumps({'status':'ok'}))
    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'User not authenticated'}))


def dashboard(request):
    if request.user.is_authenticated():
        sign_up_sign_in(request, android_user=False)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def landing(request):
    if request.user.is_authenticated():
        from apps.exam_api.views import ExamHandler
        exam_handler = ExamHandler()
        upcoming_exams = exam_handler.list_upcoming_exams()
        parameters = {}        
        up_exams = []

        user_profile_obj = UserProfile()
        subscribed_exams = user_profile_obj.get_subscribed_exams(request.user.username)
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user

        subscription_type = user['subscription_type']

        if len(subscription_type) !=0:
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
                up_exm['subscribed'] = eachExam['exam_code'] in subscribed_exams

            up_exm['code'] = eachExam['exam_code']
            if eachExam['exam_family'] != 'DPS':
                up_exm['exam_time'] = eachExam['exam_time']
                up_exm['exam_date'] = datetime.datetime.fromtimestamp(int(eachExam['exam_date'])).strftime("%A, %d. %B %Y")
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
        #     up_sch['schedule_date'] = datetime.datetime.fromtimestamp(int(eachSchedule['schedule_date'])).strftime("%A, %d. %B %Y")
        #     up_schedules.append(up_sch)
        # parameters['upcoming_schedules'] = up_schedules

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
        parameters['has_result'] = False
        return render_to_response('dashboard.html',parameters,
                              context_instance=RequestContext(request))
    else:
        return render_to_response('landing.html', context_instance=RequestContext(request))

def attend_exam(request,exam_code):
    user_profile_obj = UserProfile()
    subscribed = user_profile_obj.check_subscribed(request.user.username, exam_code)
    if request.user.is_authenticated() and subscribed:
        parameters = {}
        ess = ExamStartSignal()        
        exam_obj = ExammodelApi()

        exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})
        validate = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1})
        end_validate = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1, 'end':1})        

        atte_ans = AttemptedAnswerDatabase()
        all_answers = atte_ans.find_all_atttempted_answer({
            'exam_code':exam_code, 'user_id':int(request.user.id),
            'ess_starttimestamp':int(validate['start_time'])})
        parameters['all_answers'] = json.dumps(all_answers)

        if end_validate !=None:
            if exam_details['exam_family'] == 'CPS':
                return HttpResponseRedirect('/results/' + str(exam_code) +'/')
            else:
                parameters['all_answers'] = []

        else:
            if validate != None:
                time_elapsed = time.mktime(datetime.datetime.now().timetuple()) - validate['start_time']
                if time_elapsed > exam_details['exam_duration']*60 and exam_details['exam_family']=='CPS':
                    return HttpResponseRedirect('/results/' + str(exam_code) +'/')
                elif time_elapsed > exam_details['exam_duration']*60 and exam_details['exam_family']!='CPS':
                    parameters['all_answers'] = []
            exam_details['exam_duration'] = exam_details['exam_duration'] - time_elapsed/60
        
        try:
            honor_code_accept = request.session[str(exam_code)]
        except:
            honor_code_accept = False

        if not honor_code_accept:
            return HttpResponseRedirect('/honorcode/'+str(exam_code) +'/')
        
        question_obj = QuestionApi()    
        questions = question_obj.find_all_questions({"exam_code": int(exam_code)})
        total_questions = question_obj.get_count({"exam_code": int(exam_code)})
        sorted_questions = sorted(questions, key=lambda k: k['question_number'])

        if exam_details['exam_family'] != 'DPS':
            exam_details['exam_date'] = datetime.datetime.fromtimestamp(int(exam_details['exam_date'])).strftime('%Y-%m-%d')

        parameters['questions'] = json.dumps(sorted_questions)
        parameters['exam_details'] = exam_details
        
        start_question_number = 0 
        try:
            start_question_number = int(request.session['current_question_number'])
            if start_question_number == '':
                start_question_number = 0
        except:
            start_question_number = 0 

        if start_question_number == total_questions:
            start_question_number = start_question_number - 1
            parameters['next_to_start'] = sorted_questions[start_question_number]
        else:            
            parameters['next_to_start'] = sorted_questions[0]
        
        parameters['start_question_number'] = start_question_number
        parameters['start_question'] = sorted_questions[start_question_number]
        parameters['max_questions_number'] =  total_questions

        parameters['exam_code'] = exam_code        
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user
        return render_to_response('exam_main.html', parameters, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def honorcode(request, exam_code):    
    exam_obj = ExammodelApi()
    exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})
    user_profile_obj = UserProfile()
    subscribed = user_profile_obj.check_subscribed(request.user.username, exam_code)
    parameters = {}
    parameters['render_before_exam'] = False
    if request.user.is_authenticated() and subscribed:
        from apps.mainapp.classes.query_database import ExamStartSignal
        ess = ExamStartSignal()            
        validate_start = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1})        
        current_time = time.mktime(datetime.datetime.now().timetuple())

        if exam_details['exam_family'] == 'CPS':
            check_time = exam_details['exam_date']
        else:
            if validate_start !=None:
                check_time = validate_start['start_time']
            else:                
                parameters['exam_details'] = exam_details
                parameters['exam_code'] = exam_code                

                user_profile_obj = UserProfile()
                user = user_profile_obj.get_user_by_username(request.user.username)
                parameters['user'] = user                
                return render_to_response('exam_tips_and_honor_code.html', parameters, context_instance=RequestContext(request))

        if (current_time - check_time)>exam_details['exam_duration']*60:
            ''' For now redirect to results page '''
            # parameters['render_after_exam'] = True            
            # return HttpResponseRedirect('/results/' + str(exam_code))
            parameters['exam_details'] = exam_details
            parameters['exam_code'] = exam_code                

            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            parameters['user'] = user                
            return render_to_response('exam_tips_and_honor_code.html', parameters, context_instance=RequestContext(request))            

        elif ((current_time - check_time) < exam_details['exam_duration']*60) and (current_time > check_time):
            '''render honor code'''
            try:
                if validate_start != None:
                    honor_code_accept = request.session[str(exam_code)]
                    if honor_code_accept == True:
                        return HttpResponseRedirect('/attend-exam/'+ exam_code +'/')
            except:
                pass
            if exam_details['exam_family'] !='DPS':
                exam_details['exam_date'] = datetime.datetime.fromtimestamp(int(exam_details['exam_date'])).strftime('%Y-%m-%d')
            parameters['exam_details'] = exam_details
            parameters['exam_code'] = exam_code                

            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            parameters['user'] = user
            return render_to_response('exam_tips_and_honor_code.html', parameters, context_instance=RequestContext(request))

        else:
            parameters['render_before_exam'] = True
            exam_details['exam_date'] = datetime.datetime.fromtimestamp(int(exam_details['exam_date'])).strftime('%Y-%m-%d')
            parameters['exam_details'] = exam_details
            # return HttpResponse(json.dumps({'msg':'exam not started'}))
            return render_to_response('exam_tips_and_honor_code.html', parameters, context_instance=RequestContext(request))        
    else:
        return HttpResponseRedirect('/')

def subscription(request):
    parameters = {}    
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)
    parameters['user'] = user
    return render_to_response('subscription.html', parameters, context_instance=RequestContext(request))

def tos(request):
    parameters = {}
    return render_to_response('tos.html', parameters, context_instance=RequestContext(request))

def privacy(request):
    parameters = {}
    return render_to_response('privacy.html', parameters, context_instance=RequestContext(request))    

def generate_coupon(request):
    # 1. DPS (Daily Practice Set)
    # 2. CPS (Competitive Pracice Set)
    # 3. MBBS-IOM
    # 4. BE-IOE
    # 5. IDP (Inter Disciplinary Plan)
    coupon = Coupon()        
    coupon.generate_coupons('IDP')
    coupon.generate_coupons('DPS')
    coupon.generate_coupons('CPS')
    coupon.generate_coupons('BE-IOE')
    coupon.generate_coupons('MBBS-IOM')
    return HttpResponse(json.dumps({'status':'success'}))

def get_coupons(request, subscription_type):
    coupon_obj = Coupon()
    coupons = coupon_obj.get_coupons(subscription_type)
    return HttpResponse(json.dumps({'status':'ok', 'coupons':coupons}))


def results(request, exam_code):
    parameters ={}
    # exam_handler = ExamHandler()    
    # score_dict = exam_handler.check_answers(exam_code, answer_list)
    res={}
    res['exam_code'] = 102
    res['exam_name'] = 'IOE model set 1'
    res['exam_date'] = '2014-01-1'
    res['scores'] = [
        {'name':'Phyiscs', 'score':20, 'total':50}, 
        {'name':'Chemistry', 'score':15, 'total':25}, 
        {'name':'Biology', 'score':25, 'total':30}]
    parameters['result'] = res
    parameters['myrankcard'] = {'total':200, 'rank':1}
    return render_to_response('results.html', parameters, context_instance=RequestContext(request))