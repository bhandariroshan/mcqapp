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
        parameters['current_question_number'] = 0
        parameters['questions'] = questions
        parameters['start_question'] = questions[0]        
        parameters['exam_code'] = exam_code
        return render(request, self.template_name, parameters)
