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
                #if coupon_code != 'IDP' or 'BE-IOE-071' or 'MBBS-IOM-071' then save the exam code in the valid exams
                if   'IDP' not in subscription_type and 'BE-IOE-071' not in subscription_type and 'MBBS-IOM-071' not in subscription_type:
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
            save_user_answers(request)
            # if request.session.get('has_commented', False):
            request.session['current_question_number'] = request.POST.get('current_question_number','')
            request.session['exam_code'] = request.POST.get('exam_code','')
            return HttpResponse(json.dumps({'status':'ok', 'message':'Answer successfully saved'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))
    
    def honor_code_accept(self, request):
        if request.user.is_authenticated():
            exam_code = request.POST.get('exam_code','')
            request.session[exam_code] = True
            return HttpResponse(json.dumps({'status':'ok', 'url':'/attend-exam/'+exam_code+'/'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized for this action'}))