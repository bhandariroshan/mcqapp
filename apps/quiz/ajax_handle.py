# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse


class AjaxHandle():
    """doc string for AjaxHandle"""
    def __init__(self):
        pass

    def save_answer(self, request):
    	from .load_quiz_answers import SaveQuiz
    	quiz_ans_obj = SaveQuiz()
    	quiz_ans_obj.save_user_quiz(request)