from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
# from apps.mainapp.classes.Userprofile import UserProfile
from .models import QuizResult
from datetime import datetime, timedelta


class QuizResultAdminView(View):
    template_name = 'quiz/quiz_result_admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request, *args, **kwargs):
        parameters = {}
        # user_profile_obj = UserProfile()
        # user = user_profile_obj.get_user_by_username(request.user.username)
        # ioe_results = QuizResult.objects.filter(quiz_type="BE-IOE").order_by('attempted_date')
        # iom_results = QuizResult.objects.filter(quiz_type="MBBS-IOM").order_by('attempted_date')
        all_results = QuizResult.objects.all().order_by('attempted_date')
        # for each in ioe_results:
        #     each['attempted_date'] = datetime.datetime.fromtimestamp(
        #         int(each['attempted_date'])
        #     )
        final_result = []
        for each_result in all_results:
            index = -1
            each_result['attempted_date'] = datetime.fromtimestamp(
                int(each_result['attempted_date'])
            ).date()
            for count, each in enumerate(final_result):
                if each['attempted_date'] == each_result['attempted_date']:
                    index = count
            if index != -1:
                final_result[index]['item'].append(each_result)
            else:
                final_result.append({
                    'date': each_result['attempted_date'],
                    'item': [each_result]
                })
        # parameters['ioe_results'] = ioe_results
        # parameters['ioe_results'] = ioe_results
        parameters['final_result'] = final_result
        parameters['today'] = datetime.today().date()
        parameters['yesterday'] = parameters['today'] - timedelta(1)
        return render(request, self.template_name, parameters)
