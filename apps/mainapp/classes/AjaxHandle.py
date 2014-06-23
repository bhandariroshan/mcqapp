# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
import json
from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
import datetime, time
from apps.exam_api.views import ExamHandler
from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi



from apps.mainapp.classes.query_database import ExamStartSignal
from apps.mainapp.classes.query_database import HonorCodeAcceptSingal 
from apps.mainapp.classes.query_database import AttemptedAnswerDatabase,CurrentQuestionNumber

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

    def get_nexp_page_of_questions(self, request):        
        user_profile_obj = UserProfile()
        exam_code = int(request.POST['exam_code'])
        subscribed = user_profile_obj.check_subscribed(request.user.username, exam_code)
        if request.user.is_authenticated() and subscribed:
            user_det = user_profile_obj.get_user_by_username(request.user.username)
            parameters = {}
            parameters['user'] = user_det
            ess = ExamStartSignal()        
            exam_obj = ExammodelApi()
            ess = ExamStartSignal()            

            exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})
            current_time = time.mktime(datetime.datetime.now().timetuple())

            validate_start = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1,'end':0})        
            
            if validate_start != None:
                check = validate_start['start_time']
            else:
                ess.update_exam_start_signal({
                    'exam_code':int(exam_code), 
                    'useruid':request.user.id},{
                    'start':1, 
                    'start_time':int(time.mktime(datetime.datetime.now().timetuple())),
                    'end':0,                
                    'end_time':''
                    })
                validate_start = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1, 'end':0})        
                check = validate_start['start_time']

            dps_exam_start = exam_details['exam_family']=='DPS' and current_time - check > exam_details['exam_duration']*60
            if current_time - check > exam_details['exam_duration']*60:            
                ess.update_exam_start_signal({
                    'exam_code':int(exam_code), 
                    'useruid':request.user.id, 
                    'start':1},{'end':1,'start':0, 
                    'end_time':int(time.mktime(datetime.datetime.now().timetuple()))})
                ess.update_exam_start_signal({
                    'exam_code':int(exam_code), 
                    'useruid':request.user.id},{
                    'start':1, 
                    'start_time':int(time.mktime(datetime.datetime.now().timetuple())),
                    'end':0,                
                    'end_time':''
                    })
                validate_start = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id, 'start':1,'end':0})        
                check = validate_start['start_time']
                

            if current_time - check < exam_details['exam_duration']*60:
                atte_ans = AttemptedAnswerDatabase()
                all_answers = atte_ans.find_all_atttempted_answer({
                    'exam_code':int(exam_code), 'user_id':int(request.user.id),
                    'ess_time':int(validate_start['start_time'])})
                time_elapsed = time.mktime(datetime.datetime.now().timetuple()) - validate_start['start_time']
                exam_details['exam_duration'] = (exam_details['exam_duration']*60 - time_elapsed)/60

                parameters['all_answers'] = json.dumps(all_answers)                        
                question_obj = QuestionApi()    

                
                current_pg_num = 1
                next_page = 0

                if request.POST.get('current','') !='':
                    current_pg_num = int(request.POST.get('current',''))

                if request.POST.get('next','') !='':
                    next_page = int(request.POST.get('next',''))            

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
                questions = question_obj.get_paginated_questions({"exam_code": int(exam_code), 'marks':1}, fields={'answer.correct':0}, page_num = current_pg_num)
                total_questions = question_obj.get_count({"exam_code": int(exam_code), 'marks':1})
                sorted_questions = sorted(questions, key=lambda k: k['question_number'])  


                # parameters['questions'] = json.dumps(sorted_questions)            
                parameters['questions'] = sorted_questions
                parameters['exam_details'] = exam_details
            
                start_question_number = 0 
                cqn = CurrentQuestionNumber()
                current_q_no = cqn.check_current_question_number({
                    'exam_code':int(exam_code), 
                    'useruid':request.user.id, 
                    'ess_time':validate_start['start_time']})
                parameters['max_questions_number'] =  total_questions

                parameters['exam_code'] = exam_code        
                user_profile_obj = UserProfile()
                user = user_profile_obj.get_user_by_username(request.user.username)
                parameters['user'] = user
                html =  str(render_to_response('ajax_exammain.html', parameters, context_instance=RequestContext(request)))
                html = html.replace('Content-Type: text/html; charset=utf-8', '')
                return HttpResponse(json.dumps({'status':'ok', 'html':html}))            
        else:
            return HttpResponse(json.dumps({'status':'error','message':'You are not authorized to perform this action.'}))

    def load_result(self, request):
        parameters ={}
        res={}
        exam_code = int(request.POST['exam_code'])    
        res['exam_code'] = exam_code
        exam_obj = ExammodelApi()
        exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})
        res['exam_details'] = exam_details
        ess = ExamStartSignal()            
        ess_check = ess.check_exam_started({'exam_code':int(exam_code), 'useruid':request.user.id})

        question_obj = QuestionApi()    
        total_questions = question_obj.get_count({"exam_code": int(exam_code), 'marks':1})

        ans = AttemptedAnswerDatabase()
        try:
            all_ans = ans.find_all_atttempted_answer({
                'exam_code':int(exam_code), 
                'user_id':request.user.id,
                'ess_time':ess_check['start_time']
                }, fields={'q_no':1, 'attempt_details':1})
        except:
            all_ans = ''
        answer_list = ''
        anss = []

        print all_ans

        for eachAns in all_ans:
            anss.append(eachAns['q_no'])

        for i in range(1,total_questions):       
            try:
                if i in anss:
                    answer_list += all_ans[anss.index(i)]['attempt_details'][0]['selected_ans']
                else:
                    answer_list +='e'
            except:
                answer_list += 'e'

        print len(answer_list), answer_list
        exam_handler = ExamHandler()    
        score_dict = exam_handler.check_answers(exam_code, answer_list)
        parameters['result'] = score_dict
        parameters['exam_code'] = exam_code
        parameters['myrankcard'] = {'total':200, 'rank':1}
        html =  str(render_to_response('ajax_results.html', parameters, context_instance=RequestContext(request)))
        html = html.replace('Content-Type: text/html; charset=utf-8', '')
        return HttpResponse(json.dumps({'status':'ok', 'html':html})) 


    