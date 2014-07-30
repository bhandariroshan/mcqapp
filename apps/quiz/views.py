from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from .question_quiz import GenerateQuiz
import json
from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi,\
    ExamStartSignal, HonorCodeAcceptSingal, AttemptedAnswerDatabase,\
    CurrentQuestionNumber


def generate_quiz(request, exam_type):
    print "Roshan"
    quiz_obj = GenerateQuiz()
    quiz = quiz_obj.generate_new_quiz(exam_type)
    return HttpResponse(json.dumps({'status':'Quiz Generated'}))

class QuizView(View):   
    template_name = 'exam_main.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuizView, self).get_context_data(**kwargs)
        return context

    # @method_decorator(login_required(login_url=reverse_lazy('home_page')))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SingleQuizView(View):   
    template_name = 'quiz/quiz_main.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context        
        context = super(QuizView, self).get_context_data(**kwargs)        
        return context

    @method_decorator(login_required)
    def get(self, request, exam_category, *args, **kwargs):
        parameters ={}
        question_quiz_obj = GenerateQuiz()
        exam_code, questions = question_quiz_obj.return_quiz_questions(exam_category)
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
        print questions[0]['uid']['id']
        parameters['all_answers'] = json.dumps(all_answers)
        return render(request, self.template_name, parameters)



@csrf_exempt
def ajax_request(request, func_name):
    from .ajax_handle import AjaxHandle
    ajax_handle = AjaxHandle()
    return_msg = getattr(ajax_handle, func_name)(request)
    return return_msg
