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
        all_results = QuizResult.objects.all().order_by('-attempted_date', '-quiz_score')
        final_result = []
        for each_result in all_results:
            index = -1
            each_result['attempted_date'] = datetime.fromtimestamp(
                int(each_result['attempted_date'])
            ).date()
            for count, each in enumerate(final_result):
                if each['date'] == each_result['attempted_date']:
                    index = count
            myuser = user_profile_obj.get_user_by_userid(int(each_result['user_id']))
            copy_result = {i: each_result[i] for i in each_result}
            copy_result['name'] = myuser['first_name'] + ' ' + myuser['last_name']
            copy_result['username'] = myuser['username']
            copy_result['facebook_link'] = "http://facebook.com/" + myuser['id']
            copy_result['email'] = myuser['email']
            if index != -1:
                if each_result['quiz_type'] == 'BE-IOE':
                    final_result[index]['item'][0]['result'].append(copy_result)
                else:
                    final_result[index]['item'][1]['result'].append(copy_result)
            else:
                if each_result['quiz_type'] == 'BE-IOE':
                    final_result.append({
                        'date': copy_result['attempted_date'],
                        'item': [{'result': [copy_result]}, {'result': []}]
                    })
                else:
                    final_result.append({
                        'date': copy_result['attempted_date'],
                        'item': [{'result': []}, {'result': [copy_result]}]
                    })
        # parameters['ioe_results'] = ioe_results
        # parameters['ioe_results'] = ioe_results
        parameters['final_result'] = final_result
        parameters['today'] = datetime.today().date()
        parameters['yesterday'] = parameters['today'] - timedelta(1)
        return render(request, self.template_name, parameters)
