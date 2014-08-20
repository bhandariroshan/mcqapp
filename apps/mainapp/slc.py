import time, datetime
import json
from bson.objectid import ObjectId
import requests, urllib2, urllib, cookielib
from Extract import extract
from django.http import HttpResponseRedirect, HttpResponse
from apps.mainapp.classes.SLCData import ResultRequest, ResultRequestSuccess


def find_result(request): 
    if request.method == "GET":
        cookie_jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        urllib2.install_opener(opener)

        number = request.GET.get('number')
        dob = request.GET.get('dob')
        eyear = request.GET.get('eyear')
        submit = request.GET.get('submit')
        device_id = request.POST.get('deviceId')
        uuid = request.POST.get('uuid')
        email = request.POST.get('email')
        phone = request.POST.get('phone')


        result_request = ResultRequest()
        result_request.save_result_request_data({
                'number':number, 
                'dob':dob, 
                'eyear':eyear,
                'submit':submit,
                'device_id':device_id,
                'uuid':uuid,
                'email':email,
                'phone':phone
            })

        # do POST
        if eyear != '70':
            base_url = 'http://verify.soce.gov.np/index.php'
        else:
            base_url = 'http://slc.ntc.net.np'

        values = dict(number=str(number), dob=str(dob), eyear=str(eyear), submit='Search')
        data = urllib.urlencode(values)
        req = urllib2.Request(base_url, data)
        rsp = urllib2.urlopen(req)
        content = rsp.read()


        result = extract(content)

        if result.get('status') == "ok":
            result_request_success = ResultRequestSuccess()
            result_request_success.save_result_request_success_data({
                'number':number, 
                'dob':dob, 
                'eyear':eyear,
                'submit':submit,
                'device_id':device_id,
                'uuid':uuid,
                'email':email,
                'phone':phone,
                'result':result
            })
            return HttpResponse(json.dumps({'status':'ok', 'data':result}))

        elif result.get('status') == "error":
            return HttpResponse(json.dumps({'status':'error', 'message':'Unknown error occurred in the server. Please try again later.'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Invalid Date of Birth or Symbol Number of Exam Year.'}))

    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized to perform this action.'}))        