from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.mainapp.classes.Exams import Exam, RankCard, ScoreCard
from apps.mainapp.classes.Schedules  import Schedules
import time, datetime
from django.http import HttpResponse
from apps.mainapp.classes.query_database import QuestionApi

import json

def dashboard(request):
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
        parameters['rank_card'] = rank_card[0]

        score_card_obj = ScoreCard()
        socre_card = score_card_obj.get_score_card(request.user.id, 'IOMMBBSMODEL000')
        parameters['socre_card'] = socre_card[0]        
        return render_to_response('dashboard.html',parameters,
                              context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def attempt_question(request):
    return render_to_response('qone-one.html',context_instance=RequestContext(request))


def landing(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/test/')
    return render_to_response('landing.html', context_instance=RequestContext(request))

def attend_exam(request,exam_code):
    question_obj = QuestionApi()    
    questions = question_obj.find_all({"exam_code": int(exam_code)})
    sorted_questions = sorted(questions, key=lambda k: k['question_number'])

    exam_obj = Exam()
    exam_details = exam_obj.get_exam_detail(exam_code)

    parameters = {}
    parameters['questions'] = json.dumps(sorted_questions)
    parameters['exam_details'] = exam_details
    print sorted_questions
    question_start = 0
    parameters['start_question'] = sorted_questions[0]
    print parameters['start_question']
    parameters['exam_code'] = exam_code
    return render_to_response('exam.html', parameters, context_instance=RequestContext(request))
