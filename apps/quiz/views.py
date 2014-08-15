import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.mainapp.classes.query_database import AttemptedAnswerDatabase
from apps.mainapp.classes.Userprofile import UserProfile

from .question_quiz import GenerateQuiz
from .user_quiz_data import SaveQuiz
from .user_leaderboard import LeaderBoard


class QuizGenerate(View):

    def get(self, request, exam_type, *args, **kwargs):
        quiz_obj = GenerateQuiz()
        if quiz_obj.generate_new_quiz(exam_type):
            return HttpResponse(json.dumps({'status': 'Quiz Generated'}))
        else:
            return HttpResponse(json.dumps({'Error': 'Quiz not generated'}))


class QuizView(View):
    template_name = 'quiz/quiz_landing.html'

    # @method_decorator(login_required(login_url=reverse_lazy('home_page')))
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            parameters = {}
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            ref_id = request.GET.get('refid', '')
            
            if ref_id != '':
                request.session['ref_id'] = ref_id

            if user['student_category_set'] == 0:
                return HttpResponseRedirect('/')
            else:
                if user['student_category'] == 'BE-IOE':
                    parameters['ioe_user'] = True
                else:
                    parameters['iom_user'] = True
                parameters['user'] = user
                return render(request, self.template_name, parameters)
        else:
            return render(request, self.template_name)


class SingleQuizView(View):
    template_name = 'quiz/quiz_main.html'

    @method_decorator(login_required)
    def get(self, request, exam_category, *args, **kwargs):
        parameters = {}
        question_quiz_obj = GenerateQuiz()
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user
        try:
            question_quiz_obj.return_quiz_questions(exam_category)
        except:
            raise Http404
        exam_model = question_quiz_obj.exam_model
        exam_code = exam_model['exam_code']

        quiz_ans_obj = SaveQuiz()
        check_submitted = quiz_ans_obj.check_quiz_submitted(request, int(exam_code))

        if check_submitted:
            return HttpResponseRedirect('/quiz/myscore/')
        question_list = question_quiz_obj.question_list
        parameters['quiz_details'] = exam_model
        parameters['start_question_number'] = 0
        parameters['questions'] = json.dumps(question_list)
        parameters['start_question'] = question_list[0]
        parameters['max_questions_number'] = len(question_list)
        parameters['exam_code'] = exam_code
        atte_ans = AttemptedAnswerDatabase()
        all_answers = atte_ans.find_all_atttempted_answer({
            'exam_code': int(exam_code),
            'user_id': int(request.user.id),
        })
        if all_answers == []:
            for i in range(len(question_list)):
                all_answers.append('NA')

        parameters['all_answers'] = json.dumps(all_answers)
        return render(request, self.template_name, parameters)


class QuizScore(View):
    template_name = 'quiz/quiz_score.html'

    def get(self, request, *args, **kwargs):
        parameters = {}

        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user

        leader_board = LeaderBoard()
        leader_board.user_quiz_result(request)

        if user['student_category'] == 'BE-IOE':
            parameters['ioe_user'] = True
        else:
            parameters['iom_user'] = True
        parameters['user'] = user
        parameters['user_leaderboard'] = leader_board
        return render(request, self.template_name, parameters)


class AjaxRequest(View):

    def post(self, request, func_name, *args, **kwargs):

        from .ajax_handle import AjaxHandle
        ajax_handle = AjaxHandle()
        return_msg = getattr(ajax_handle, func_name)(request)
        return return_msg
