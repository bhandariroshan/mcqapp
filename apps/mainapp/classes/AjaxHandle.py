# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
import json
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
import datetime, time
from apps.mainapp.classes.query_database import ExammodelApi

from apps.mainapp.classes.query_database import ExamStartSignal
from apps.mainapp.classes.query_database import HonorCodeAcceptSingal

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


class AjaxHandle():
    """docstring for AjaxHandle"""
    def __init__(self):
        pass

    def validate_coupon(self,request):      
        if request.user.is_authenticated():
            coupon_obj = Coupon()
            exam_code = request.POST.get('exam_code','')
            coupon_code = request.POST.get('coupon_code','')
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            from apps.mainapp.classes.Exams import Exam            
            exam_obj = Exam()
            if exam_code !='subs':
                up_exm = exam_obj.get_exam_detail(int(exam_code))
            else:                
                if coupon_obj.has_susbcription_plan_in_coupon(coupon_code):
                    coupon_obj.change_used_status_of_coupon(coupon_code, request.user.username) 
                    user_profile_obj.change_subscription_plan(request.user.username, coupon_code)                
                    user_profile_obj.save_coupon(request.user.username, coupon_code)
                    return HttpResponse(json.dumps({'status':'ok','url':'/'}))
                else:
                    return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))


            if coupon_obj.validate_coupon(coupon_code, up_exm['exam_category'], up_exm['exam_family']) == True:
                #save the coupon code in user's couponcode array 
                coupon_obj.change_used_status_of_coupon(coupon_code, request.user.username) 
                user_profile_obj.change_subscription_plan(request.user.username, coupon_code)                
                user_profile_obj.save_coupon(request.user.username, coupon_code)

                #Refreshment of user
                user = user_profile_obj.get_user_by_username(request.user.username)
                subscription_type = user['subscription_type']
                #if coupon_code != 'IDP' or 'BE-IOE' or 'MBBS-IOM' then save the exam code in the valid exams
                if   'IDP' not in subscription_type and 'BE-IOE' not in subscription_type and 'MBBS-IOM' not in subscription_type:
                    user_profile_obj.save_valid_exam(request.user.username, exam_code)                    

                if 'IDP' in subscription_type:
                    return HttpResponse(json.dumps({'status':'ok','url':'/honorcode/' + exam_code}))

                elif up_exm['exam_category']  in subscription_type:
                    return HttpResponse(json.dumps({'status':'ok','url':'/honorcode/' + exam_code}))
                else:
                    subscribed_exams = user_profile_obj.get_subscribed_exams(request.user.username)
                    if int(exam_code) in subscribed_exams:
                        #Check if exam is cps or dps 
                        #if exam is cps then return url '/cps/exam_code'
                        #else return  url '/dps/exam_code/'
                        print "Roshan Bhandari and DPS"
                        return HttpResponse(json.dumps({'status':'ok','url':'/dps/' + exam_code}))
                    else:
                        return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))
            else:
                return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))
        else:
            return HttpResponse(json.dumps({'status':'error','message':'You are not authorized to perform this action.'}))

    def is_subscribed(self, request):      
        if request.user.is_authenticated():
            coupon_obj = Coupon()
            exam_code = request.POST.get('exam_code','')
            user_id = request.user.id

            if exam_code.strip() == 'sample':
                return HttpResponse(json.dumps({'status':'error','message':'not subscribed'}))
            else:
                if coupon_obj.check_subscried(exam_code,user_id):                
                    return HttpResponse(json.dumps({'status':'ok', 'url':'/honorcode/'+ exam_code + '/'}))
                else:
                    return HttpResponse(json.dumps({'status':'error','message':'not subscribed'}))
        else:
            return HttpResponse(json.dumps({'status':'error','message':'You are not authorized to perform this action.'}))

    def save_answer(self, request):
        if request.user.is_authenticated():
            from apps.exam_api.views import save_user_answers
            from apps.mainapp.classes.query_database import ExamStartSignal, CurrentQuestionNumber
            ess = ExamStartSignal()
            exam_code =request.POST.get('exam_code','')
            validate = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1,'end':0})
            if validate != None:
                from apps.mainapp.classes.query_database import ExammodelApi
                ema = ExammodelApi()
                exam_details = ema.find_one_exammodel({'exam_code':int(exam_code)})
                if exam_details['exam_family'] == 'CPS':
                    time_elapsed = time.mktime(datetime.datetime.now().timetuple()) - exam_details['exam_date']
                else:
                    time_elapsed = time.mktime(datetime.datetime.now().timetuple()) - validate['start_time']
                time_remained = (exam_details['exam_duration']*60 - time_elapsed)/60
                '''check if user time has expired or not '''
                if time_elapsed > exam_details['exam_duration']*60:
                    return HttpResponse(json.dumps({'status':'TimeElapsedError', 'message':'Time has elapsed'}))
                else:
                    save_user_answers(request, int(validate['start_time']))
                    # if request.session.get('has_commented', False):
                    cqn = CurrentQuestionNumber()
                    cqn.update_current_question_number({
                        'ess_time':int(validate['start_time']),
                        'exam_code':int(exam_code),
                        'useruid':request.user.id
                        }, {'cqn':int(request.POST.get('current_question_number',''))+1})
                    request.session['exam_code'] = request.POST.get('exam_code','')
                    return HttpResponse(json.dumps({'status':'ok', 'message':'Answer successfully saved', 'time_remained':time_remained}))

            else:
                return HttpResponse(json.dumps({'status':'error', 'message':'Exam not Validated'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))
    
    def honor_code_accept(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code','')
            request.session[exam_code] = True

            ess = ExamStartSignal()
            exam_obj = ExammodelApi()
            exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})            
            exam_duration = exam_details['exam_duration'] * 60


            validate = ess.check_exam_started({
                'exam_code':int(exam_code), 
                'useruid':request.user.id, 
                'start':1, 
                'end':0})
            
            start_time = datetime.datetime.now().timetuple()                        
            start_time = time.mktime(start_time)

            h_a_s = HonorCodeAcceptSingal()
            h_a_s.update_honor_code_accept_Signal({'useruid':request.user.id, 
                'exam_code':int(exam_code), 'ess_time':int(start_time)},{'accept':1})
            print validate
            ess.insert_exam_start_signal({
                'exam_code':int(exam_code), 
                'useruid':request.user.id, 
                'start':1, 
                'start_time':int(start_time),
                'end':0
            })
            return HttpResponse(json.dumps({'status':'ok', 'url':'/cps/'+ exam_code + '/'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))

    
    def set_exam_finished(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code','')
            redirect = request.POST.get('redirect','')
            ess = ExamStartSignal()
            end_time = datetime.datetime.now().timetuple()                        
            end_time = time.mktime(end_time) 

            validate = ess.check_exam_started({
                'exam_code':int(exam_code), 
                'useruid':request.user.id, 
                'start':1, 
                'end':0})           
            
            h_a_s = HonorCodeAcceptSingal()
            try:
                h_a_s.update_honor_code_accept_Signal({
                    'useruid':request.user.id, 
                    'exam_code':int(exam_code), 
                    'ess_time':int(validate['start_time'])},{'accept':0})            
            except:
                pass

            ess.update_exam_start_signal({
                'exam_code':int(exam_code), 
                'useruid':request.user.id, 
                'start':1},{'end':1,'start':0, 'end_time':end_time})
            request.session['current_question_number'] = ''
            if redirect=='1':
                return HttpResponse(json.dumps({'status':'ok', 'redirect':1 ,'url':'/results/'+exam_code+'/'}))
            else:
                return HttpResponse(json.dumps({'status':'ok', 'redirect':0}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))

    def save_category(self, request):
        user =  UserProfile()
        if request.user.is_authenticated():
            ioe_check = bool(request.POST.get('ioe_check', ''))
            iom_check = bool(request.POST.get('iom_check', ''))
            if ioe_check and iom_check:
                cat = 'IDP'
            elif ioe_check:
                cat = 'BE-IOE'
            elif iom_check:
                cat = 'MBBS-IOM'
            user.update_upsert({'username':request.user.username}, {'student_category':cat, 'student_category_set':1})
            return HttpResponse(json.dumps({'status':'ok'}))
        else:
            return HttpResponse(json.dumps({'status':'error','message':'You are not authorized to perform this action.'}))

    