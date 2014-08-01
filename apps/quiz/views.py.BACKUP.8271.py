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


<<<<<<< HEAD
class QuizView(View):
    template_name = 'exam_main.html'
=======
class QuizView(View):   
    template_name = 'quiz/quiz_landing.html'
>>>>>>> 39b10aaee4102033cedd07f87df5e1b358274118

    # @method_decorator(login_required(login_url=reverse_lazy('home_page')))
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            parameters ={}
            from apps.mainapp.classes.Userprofile import UserProfile
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
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
        from apps.mainapp.classes.Userprofile import UserProfile
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user
        exam_model, questions = question_quiz_obj.return_quiz_questions(exam_category)
        exam_code = exam_model['exam_code']
        parameters['quiz_details'] = exam_model

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
<<<<<<< HEAD
        leader_board = LeaderBoard()
        leader_board.user_quiz_result(request)
        parameters['user_leaderboard'] = leader_board

=======
        from apps.mainapp.classes.Userprofile import UserProfile
        
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user

        from .user_leaderboard import LeaderBoard
        leader_board = LeaderBoard()
        user_leaderboard = leader_board.user_quiz_result(request)

        ioe_quiz_result = []
        iom_quiz_result = []

        for eachResult in user_leaderboard['ioe_quiz_result']:            
            eachResult['attempted_date'] =  datetime.datetime.fromtimestamp(int(eachResult['attempted_date'])).strftime('%Y-%m-%d')
            ioe_quiz_result.append(eachResult)

        for eachResult in user_leaderboard['iom_quiz_result']:
            eachResult['attempted_date'] =  datetime.datetime.fromtimestamp(int(eachResult['attempted_date'])).strftime('%Y-%m-%d')
            iom_quiz_result.append(eachResult)
            
        if user['student_category'] == 'BE-IOE':
            parameters['ioe_user'] = True
        else:
            parameters['iom_user'] = True
        parameters['user'] = user
        parameters['iom_quiz_result'] = iom_quiz_result
        parameters['ioe_quiz_result'] = ioe_quiz_result
        parameters['iom_total_score'] = user_leaderboard['iom_total_score']
        parameters['ioe_total_score'] = user_leaderboard['ioe_total_score']
>>>>>>> 39b10aaee4102033cedd07f87df5e1b358274118
        return render(request, self.template_name, parameters)


class AjaxRequest(View):
    def post(self, request, func_name, *args, **kwargs):
        ajax_handle = AjaxHandle()
        return_msg = getattr(ajax_handle, func_name)(request)
        return return_msg
