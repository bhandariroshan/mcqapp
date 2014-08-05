from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from apps.mainapp.classes.Userprofile import UserProfile
from .models import QuizResult
from datetime import datetime, timedelta


class QuizResultAdminView(View):
    template_name = 'quiz/quiz_result_admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request, *args, **kwargs):
        parameters = {}
        user_profile_obj = UserProfile()
        all_results = QuizResult.objects.all().order_by('-quiz_score')
        final_result = []
        for each_result in all_results:
            index = -1
            each_result['attempted_date'] = datetime.fromtimestamp(
                int(each_result['attempted_date'])
            ).date()
            for count, each in enumerate(final_result):
                if each['date'] == each_result['attempted_date']:
                    index = count
            if index != -1:
                if each_result['quiz_type'] == 'BE-IOE':
                    final_result[index]['item'][0]['result'].append(each_result)
                else:
                    final_result[index]['item'][1]['result'].append(each_result)
            else:
                if each_result['quiz_type'] == 'BE-IOE':
                    myuser = user_profile_obj.get_user_by_userid(int(each_result['user_id']))
                    each_result['name'] = myuser['first_name'] + ' ' + myuser['last_name']
                    each_result['username'] = myuser['username']
                    each_result['facebook_link'] = myuser['link']
                    each_result['email'] = myuser['email']
                    final_result.append({
                        'date': each_result['attempted_date'],
                        'item': [{'result': [each_result]}, {'result': []}]
                    })
                else:
                    final_result.append({
                        'date': each_result['attempted_date'],
                        'item': [{'result': []}, {'result': [each_result]}]
                    })
        # parameters['ioe_results'] = ioe_results
        # parameters['ioe_results'] = ioe_results
        parameters['final_result'] = final_result
        parameters['today'] = datetime.today().date()
        parameters['yesterday'] = parameters['today'] - timedelta(1)
        return render(request, self.template_name, parameters)
