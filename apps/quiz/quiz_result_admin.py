from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from apps.mainapp.classes.Userprofile import UserProfile
from .models import QuizResult


class QuizResultAdminView(View):
    template_name = 'quiz/quiz_result_admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request, *args, **kwargs):
        parameters = {}
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        all_results = QuizResult.objects.all().order_by('attempted_date')
        for each in all_results:
            print each.attempted_date
        parameters['all_results'] = all_results
        return render(request, self.template_name, parameters)
