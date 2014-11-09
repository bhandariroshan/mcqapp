from django.http import HttpResponse
from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from apps.mainapp.classes.Userprofile import UserProfile
from apps.exam_api.views import ExamHandler
import time, datetime
from django.contrib.auth.decorators import user_passes_test, login_required


@login_required
def subject_wise_test_ui(request, subject_name):
    parameters = {}
    user_profile_obj = UserProfile()
    user = user_profile_obj.get_user_by_username(request.user.username)

    if user is None:
        raise Http404

    parameters['user'] = user

    parameters['subject_name'] = subject_name.capitalize()
    return render_to_response(
            'subject-inter.html', parameters, context_instance=RequestContext(request)
        )

def attend_subject_wise_test(request, subject_name):    
    user_profile_obj = UserProfile()
    genereate_exam_message = user_profile_obj.check_generate_and_save_valid_subject_exam(request.user.username, subject_name)
    if genereate_exam_message['status'] == 'ok':
        return HttpResponseRedirect('/test/dps/' + str(genereate_exam_message['exam_code']) + '/')
    else:
        parameters = {}        
        user = user_profile_obj.get_user_by_username(request.user.username)
        if user is None:
            raise Http404
        parameters['user'] = user
        parameters['subject_name'] = subject_name.capitalize()
        parameters['error'] = True
        parameters['error_message_generate_subject_exam'] = genereate_exam_message['message']
        return render_to_response(
                'subject-inter.html', parameters, context_instance=RequestContext(request)
            )


def generate_random_subject_test(subject_name):
    '''
    
    The function generates generates a random question set by randomly picking
    question from a specified subject

    '''
    question_api = QuestionApi()
    question_id_list = question_api.get_random_question_set(subject_name)


    exammodel_api = ExammodelApi()
    last_exam_code = exammodel_api.find_all_exammodel_descending(
        {},
        fields={"exam_code": 1},
        sort_index="exam_code",
        limit=1
    )
    if len(last_exam_code) > 0:
        new_exam_code = int(last_exam_code[0]['exam_code']) + 1
    else:
        new_exam_code = 10001
    new_exam_model = {
        "exam_name": str(subject_name).lower() + " test",
        "exam_date": time.mktime(
            datetime.datetime.now().timetuple()
        ),
        "image": "exam.jpg",
        "exam_code": new_exam_code,
        "exam_category": str(subject_name).lower() + "-test",
        "exam_duration": 20,
        "exam_family": 'DPS',
        "question_list": question_id_list
    }
    exammodel_api.insert_new_model(new_exam_model)
    return new_exam_code