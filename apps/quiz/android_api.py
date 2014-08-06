import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .question_quiz import GenerateQuiz


@login_required
def get_quiz_question(request, exam_category):
    """
    This function returns the list of quiz questions for the
    requested exam_category
    """
    quiz_obj = GenerateQuiz()
    quiz_obj.return_quiz_questions(exam_category)
    question_set = quiz_obj.question_list
    exam_model = quiz_obj.exam_model
    sorted_questions = sorted(
        question_set, key=lambda k: k['uid']['id']
    )
    for count, item in enumerate(sorted_questions):
        item['question_number'] = count + 1

    response = HttpResponse(json.dumps(
        {'status': 'ok',
         'result': sorted_questions,
         'exam_model_code': exam_model['exam_code']}
    ))
    return response
