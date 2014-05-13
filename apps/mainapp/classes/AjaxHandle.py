# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
import json
from apps.mainapp.classes.Coupon import Coupon

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
    		if exam_code.strip() == 'sample' and coupon_code.lower()=='sample-1234':
				return HttpResponse(json.dumps({'status':'ok','url':'/exam/'+exam_code}))    			

    		if exam_code.strip() != 'sample' and coupon_code.lower()=='sample-1234':
    			return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))

    		if coupon_obj.validate_coupon(request.POST.get('coupon_code',"false")) != None:
    			coupon_obj.change_used_status_of_coupon(coupon_code, request.user.id, exam_code)
    			return HttpResponseRedirect('/exam/'+ exam_code + '/')
    		else:
    			return HttpResponse(json.dumps({'status':'error','message':'Invalid Coupon code.'}))
    	else:
    		return HttpResponse(json.dumps({'status':'error','message':'You are not authorized to perform this action.'}))