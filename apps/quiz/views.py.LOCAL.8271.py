import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.mainapp.classes.query_database import AttemptedAnswerDatabase

from .question_quiz import GenerateQuiz
from .ajax_handle import AjaxHandle
from .user_leaderboard import LeaderBoard
from .user_quiz_data import SaveQuiz


class QuizGenerate(View):
    def get(self, request, exam_type, *args, **kwargs):
        quiz_obj = GenerateQuiz()
        quiz_obj.generate_new_quiz(exam_type)
        return HttpResponse(json.dumps({'status': 'Quiz Generated'}))


class QuizView(View):
    template_name = 'exam_main.html'

    # @method_decorator(login_required(login_url=reverse_lazy('home_page')))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SingleQuizView(View):
    template_name = 'quiz/quiz_main.html'

    @method_decorator(login_required)
    def get(self, request, exam_category, *args, **kwargs):
        parameters = {}
        question_quiz_obj = GenerateQuiz()
        exam_code, questions = question_quiz_obj.return_quiz_questions(exam_category)

        quiz_ans_obj = SaveQuiz()
        check_submitted = quiz_ans_obj.check_quiz_submitted(request, int(exam_code))

        if check_submitted:
            return HttpResponseRedirect('/quiz/myscore/')

        parameters['start_question_number'] = 0
        parameters['questions'] = json.dumps(questions)
        parameters['start_question'] = questions[0]
        parameters['max_questions_number'] = len(questions)
        parameters['exam_code'] = exam_code
        atte_ans = AttemptedAnswerDatabase()
        all_answers = atte_ans.find_all_atttempted_answer({
            'exam_code': int(exam_code),
            'user_id': int(request.user.id),
        })
        if all_answers == []:
            for i in range(0, len(questions)):
                all_answers.append('NA')

        parameters['all_answers'] = json.dumps(all_answers)
        return render(request, self.template_name, parameters)


class QuizScore(View):
    template_name = 'quiz/quiz_score.html'

    def get(self, request, *args, **kwargs):
        parameters = {}
        leader_board = LeaderBoard()
        leader_board.user_quiz_result(request)
        parameters['user_leaderboard'] = leader_board

        return render(request, self.template_name, parameters)


class AjaxRequest(View):
    def post(self, request, func_name, *args, **kwargs):
        ajax_handle = AjaxHandle()
        return_msg = getattr(ajax_handle, func_name)(request)
        return return_msg