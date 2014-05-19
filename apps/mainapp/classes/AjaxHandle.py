# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
import json
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile

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
            from apps.mainapp.classes.Exams import Exam            
            exam_obj = Exam()
            up_exm = exam_obj.get_exam_detail(exam_code)

            if exam_code.strip() == 'sample' and coupon_code.lower()=='sample-1234':
                return HttpResponse(json.dumps({'status':'ok','url':'/honorcode/100/'}))

            if exam_code.strip() != 'sample' and coupon_code.lower()=='sample-1234':
                return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))

            if coupon_obj.validate_coupon(request.POST.get('coupon_code',"false")) != None:
                coupon_obj.change_used_status_of_coupon(coupon_code)
                coupon = coupon_obj.get_coupon_by_coupon_code(coupon_code)
                
                user_profile_obj = UserProfile()
                subscribed_exams = user_profile_obj.get_subscribed_exams(request.user.username)

                user = user_profile_obj.get_user_by_username(request.user.username)
                subscription_type = user['subscription_type']

                
                if (up_exm['exam_category'] == 'BE-IOE-071' or up_exm['exam_category'] =='MBBS-IOM-071') and subscription_type=='IDP':
                    return {'status':'ok','url':'/honorcode/' + exam_code}
                elif (up_exm['exam_category'] == 'BE-IOE-071' and subscription_type =='BE-IOE-071'):
                    return {'status':'ok','url':'/honorcode/' + exam_code}
                elif (up_exm['exam_category'] == 'MBBS-IOM-071' and subscription_type=='MBBS-IOM-071'):
                    return {'status':'ok','url':'/honorcode/' + exam_code}
                else:
                    if up_exm['exam_code'] in subscrbed_exams:
                        return {'status':'ok','url':'/honorcode/' + exam_code}
                    else:
                        return {'status':'error','message':'Invalid Coupon code.'}



                user_profile_obj = UserProfile()
                user_profile_obj.save_subscribed_exam(exam_code, request.user.id)

                return HttpResponse(json.dumps({'status':'ok', 'url':'/honorcode/'+ exam_code + '/'}))
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