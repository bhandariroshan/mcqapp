# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
import json
from .user_quiz_data import SaveQuiz

class AjaxHandle():
    """doc string for AjaxHandle"""
    def __init__(self):
        pass

    def save_quiz_answer(self, request):
        if request.user.is_authenticated():
            quiz_ans_obj = SaveQuiz()
            quiz_ans_obj.save_user_quiz(request)
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps({'status':'You are not authorized to perform this action.'}))


    def set_quiz_finished(self, request):
        if request.user.is_authenticated():
            quiz_ans_obj = SaveQuiz()
            quiz_ans_obj.save_daily_quiz_score(request)
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps({'status':'You are not authorized to perform this action.'}))        
