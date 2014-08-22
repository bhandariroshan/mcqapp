import time, datetime
import json
from bson.objectid import ObjectId
import requests, urllib2, urllib, cookielib
from Extract import extract
from django.http import HttpResponseRedirect, HttpResponse
from apps.mainapp.classes.SLCData import ResultRequest, ResultRequestSuccess
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

@csrf_exempt
def find_result(request): 
    if request.method == "POST":
        cookie_jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        urllib2.install_opener(opener)

        number = request.POST.get('number')
        dob = request.POST.get('dob')
        eyear = request.POST.get('eyear')
        submit = request.POST.get('submit')
        device_id = request.POST.get('deviceId')
        uuid = request.POST.get('uuid')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        print "ROSHAN"


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
            total_full_marks = 0          
            total_theory_obtained = 0
            total_practical_obtained = 0
            total_marks_obtained = 0

            for eachScore in result['result']['scores']:
                eachScore['subject'] = eachScore['subject'].capitalize()
                total_full_marks +=100
                total_theory_obtained = total_theory_obtained + int(eachScore['theory'])
                try:
                    total_practical_obtained = total_practical_obtained + int(eachScore['practical'])
                except:
                    pass
                total_marks_obtained = total_marks_obtained + int(eachScore['total_obtained'])

            result['street'] = result['street'].capitalize()
            result['result']['total_theory_obtained'] = total_theory_obtained
            result['result']['total_practical_obtained'] = total_practical_obtained
            result['result']['total_full_marks'] = total_full_marks
            result['result']['year'] = '20' + str(eyear)

            parameters = {'result':result['result']}
            my_result_html = str(render_to_response('slcresult.html',parameters))
            my_result_html = my_result_html.replace('Content-Type: text/html; charset=utf-8', '')            
            return HttpResponse(json.dumps({'status':'ok', 'data':result['result'], 'html':my_result_html}))

        elif result.get('status') == "error":
            return HttpResponse(json.dumps({'status':'error', 'message':'Unknown error occurred in the server. Please try again later.'}))
        else:
            return HttpResponse(json.dumps({'status':'error', 'message':'Invalid Date of Birth or Symbol Number of Exam Year.'}))

    else:
        return HttpResponse(json.dumps({'status':'error', 'message':'Not Authorized to perform this action.'}))