# Create your views here.


class AjaxHandle():
    """doc string for AjaxHandle"""
    def __init__(self):
        pass

    def save_quiz_answer(self, request):
        from .user_quiz_data import SaveQuiz

        quiz_ans_obj = SaveQuiz()
        quiz_ans_obj.save_user_quiz(request)
