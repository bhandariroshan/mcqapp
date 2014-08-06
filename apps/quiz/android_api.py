import json
from bson.objectid import ObjectId

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from apps.mainapp.classes.query_database import ExammodelApi, QuestionApi

from .question_quiz import GenerateQuiz
from .models import QuizResult


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


def save_quiz_score(request):
    """
    This function receives the exam_code of the quiz and sa
    """
    IMPROPER_REQUEST = 'Could not process improper request'
    try:
        exam_code = int(request.GET.get('exam_code'))
        answer_list = list(request.GET.get('answers'))
    except Exception:
        return HttpResponse(json.dumps(
            {'status': 'error', 'message': IMPROPER_REQUEST}
        )
        )
    exam_model_obj = ExammodelApi()
    exam_model = exam_model_obj.find_one_exammodel(
        {'exam_code': int(exam_code)}
    )
    question_id_list = [
        ObjectId(i['id']) for i in exam_model['question_list']
    ]
    question_api = QuestionApi()
    question_list = question_api.find_all_questions(
        {'_id': {"$in": question_id_list}},
        fields={'answer.correct': 1},
        sort_index='_id'
    )
    quiz_score = 0
    for index, choice in enumerate(answer_list):
        if question_list[index]['answer']['correct'] == choice:
            quiz_score += 1

    exam_name = exam_model['exam_name']
    quiz_number = exam_model['quiz_number']
    quiz_result_obj = QuizResult(
        quiz_code=exam_code,
        attempted_date=exam_model['exam_date'],
        quiz_type=exam_model['exam_category']
    )
    quiz_result_obj.quiz_name = ' '.join([exam_name, str(quiz_number)])
    quiz_result_obj.user_id = request.user.id
    quiz_result_obj.quiz_score = quiz_score
    quiz_result_obj.submitted = True
    quiz_result_obj.save()
