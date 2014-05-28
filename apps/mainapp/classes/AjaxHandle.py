# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
import json
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
import datetime, time

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
                print "Roshan"
                if coupon_obj.has_susbcription_plan_in_coupon(coupon_code):
                    print "Username"
                    coupon_obj.change_used_status_of_coupon(coupon_code, request.user.username) 
                    user_profile_obj.change_subscription_plan(request.user.username, coupon_code)                
                    user_profile_obj.save_coupon(request.user.username, coupon_code)
                    return HttpResponse(json.dumps({'status':'ok','url':'/'}))
                else:
                    print "Bhandari"
                    return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))

            # if exam_code.strip() != 'sample' and coupon_code.lower()=='sample-1234':
            #     return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))

            if coupon_obj.validate_coupon(coupon_code, up_exm['exam_category'], up_exm['exam_family']) == True:
                #save the coupon code in user's couponcode array 
                coupon_obj.change_used_status_of_coupon(coupon_code, request.user.username) 
                user_profile_obj.change_subscription_plan(request.user.username, coupon_code)                
                user_profile_obj.save_coupon(request.user.username, coupon_code)

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
                    if exam_code in subscribed_exams:
                        return HttpResponse(json.dumps({'status':'ok','url':'/honorcode/' + exam_code}))
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
            from apps.mainapp.classes.query_database import ExamStartSignal
            ess = ExamStartSignal()
            exam_code =request.POST.get('exam_code','')
            validate = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1})
            if validate != None:
                from apps.mainapp.classes.query_database import ExammodelApi
                ema = ExammodelApi()
                exam_details = ema.find_one_exammodel({'exam_code':int(exam_code)})
                time_elapsed = time.mktime(datetime.datetime.now().timetuple()) - validate['start_time']
                '''check if user time has expired or not '''
                if time_elapsed > exam_details['exam_duration']*60:
                    return HttpResponse(json.dumps({'status':'TimeElapsedError', 'message':'Time has elapsed'}))
                else:
                    save_user_answers(request)
                    # if request.session.get('has_commented', False):
                    request.session['current_question_number'] = int(request.POST.get('current_question_number',''))+1
                    request.session['exam_code'] = request.POST.get('exam_code','')
                    return HttpResponse(json.dumps({'status':'ok', 'message':'Answer successfully saved'}))
            else:
                return HttpResponse(json.dumps({'status':'error', 'message':'Exam not Validated'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))
    
    def honor_code_accept(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code','')
            request.session[exam_code] = True
            from apps.mainapp.classes.query_database import ExamStartSignal
            ess = ExamStartSignal()
            print exam_code 
            print request.POST
            print int(exam_code)
            validate = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1})
            if validate == None:
                start_time = datetime.datetime.now().timetuple()                        
                start_time = time.mktime(start_time)
                ess.insert_exam_start_signal({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1, 'start_time':start_time})
            return HttpResponse(json.dumps({'status':'ok', 'url':'/attend-exam/'+exam_code+'/'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))

    
    def set_exam_finished(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code','')
            from apps.mainapp.classes.query_database import ExamStartSignal
            ess = ExamStartSignal()
            end_time = datetime.datetime.now().timetuple()                        
            end_time = time.mktime(end_time)            
            ess.insert_exam_start_signal({'exam_code':int(exam_code), 'useruid':request.user.id, 'end':1, 'end_time':end_time})
            request.session['current_question_number'] = ''
            return HttpResponse(json.dumps({'status':'ok', 'url':'/result/'+exam_code+'/'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))