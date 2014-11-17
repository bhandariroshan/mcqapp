from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .classes.Userprofile import UserProfile
from collections import Counter


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    parameters = {}
    return render_to_response('superuser/dashboard.html', context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def exam_count(request):
    parameters = {}
    count = request.GET.get('count', '100')
    all_users = User.objects.all().order_by('-date_joined')[:int(count)]
    parameters['count'] = len(User.objects.all())
    latest_users = []
    user_prof = UserProfile()
    for each in all_users:
        try:

            social_obj = SocialAccount.objects.get(
                user=each
            )

            user_details = user_prof.get_user_by_username(each.username)
            practice_exams_count = 0
            subject_exams_count = 0
            if user_details.get('valid_practice_exam') is not None:
                practice_exams_list = [i['exam_category'] for i in user_details.get('valid_practice_exam')]
                practice_exams_count = '\n'.join([str(i)+": "+ str(Counter(practice_exams_list)[i]) for i in Counter(practice_exams_list)])

            if user_details.get('valid_subject_exam') is not None:
                subject_exams_list = [i['exam_category'] for i in user_details.get('valid_subject_exam')]
                subject_exams_count = '\n'.join([str(i)+": "+ str(Counter(subject_exams_list)[i]) for i in Counter(subject_exams_list)])
            if practice_exams_count == 0 and subject_exams_count == 0:
                continue

            if each.first_name != '':
                first_name = each.first_name
            elif social_obj.extra_data.get('first_name') is not None:
                first_name = social_obj.extra_data.get('first_name')
            else:
                first_name = ''

            if each.last_name != '':
                last_name = each.last_name
            elif social_obj.extra_data.get('last_name') is not None:
                last_name = social_obj.extra_data.get('last_name')
            else:
                last_name = ''
            gender = social_obj.extra_data.get('gender')

            each_user = {
                'username': each.username,
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'email': each.email,
                'fb_url': social_obj.extra_data.get('link')
                if social_obj.extra_data.get('link') is not None else '',
                'practice_exams_count': practice_exams_count,
                'subject_exams_count': subject_exams_count
            }
            latest_users.append(each_user)
        except:
            pass
    parameters['latest_users'] = latest_users    
    return render_to_response('superuser/exam_count.html', parameters, context_instance=RequestContext(request))