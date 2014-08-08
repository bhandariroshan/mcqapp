import json
from bson.objectid import ObjectId

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from apps.mainapp.classes.query_database import ExammodelApi, QuestionApi

from .question_quiz import GenerateQuiz
from .models import QuizResult, QuizAnswer
from .user_quiz_data import SaveQuiz


@login_required
def get_quiz_question(request, exam_category):
    """
    This function returns the list of quiz questions for the
    requested exam_category
    """
    quiz_obj = GenerateQuiz()
    quiz_obj.return_quiz_questions(exam_category)
    exam_model = quiz_obj.exam_model
    exam_code = exam_model['exam_code']

    save_quiz_obj = SaveQuiz()
    if save_quiz_obj.check_quiz_submitted(request, int(exam_code)):
        response = {'status': 'error',
                    'message': 'You have already given the quiz'
                    }
    else:
        question_set = quiz_obj.question_list
        sorted_questions = sorted(
            question_set, key=lambda k: k['uid']['id']
        )
        for count, item in enumerate(sorted_questions):
            item['question_number'] = count + 1

        response = {'status': 'ok',
                    'result': sorted_questions,
                    'exam_model_code': exam_code
                    }

    return HttpResponse(json.dumps(response))


def save_quiz_score(request, exam_model, answer_list):
    """
    This function receives the exam_code of the quiz and sa
    """

    question_id_list = [
        ObjectId(i['id']) for i in exam_model['question_list']
    ]
    question_api = QuestionApi()
    question_list = question_api.find_all_questions(
        {'_id': {"$in": question_id_list}},
        fields={'answer.correct': 1},
        sort_index='_id'
    )
    daily_score = 0
    for index, choice in enumerate(answer_list):
        quiz_answer_obj, created = QuizAnswer.objects.get_or_create(
            question_id=ObjectId(question_list[index]['uid']['id']),
            user_id=request.user.id,
            attempted_date=exam_model['exam_date'],
            defaults={"attempted_option": choice, "exam_code": exam_model['exam_code']}
        )
        if not created:
            quiz_answer_obj.attempted_option = choice
            quiz_answer_obj.save()

        if question_list[index]['answer']['correct'] == choice:
            daily_score += 1

    return daily_score


def user_quiz_score(request):
    """
    This function receives the exam_code of the quiz and sa
    """
    IMPROPER_REQUEST = 'Could not process improper request'
    try:
        exam_code = int(request.POST['exam_code'])
        answer_list = list(request.POST['answers'])
    except Exception:
        return HttpResponse(json.dumps(
            {'status': 'error', 'message': IMPROPER_REQUEST}
        ))
    exam_model_obj = ExammodelApi()
    exam_model = exam_model_obj.find_one_exammodel(
        {'exam_code': int(exam_code)}
    )
    if exam_model is None:
        return HttpResponse(json.dumps(
            {'status': 'error', 'message': IMPROPER_REQUEST}
        ))

    exam_name = exam_model['exam_name']
    quiz_number = exam_model['quiz_number']
    quiz_result_obj, created = QuizResult.objects.get_or_create(
        quiz_code=exam_code, user_id=request.user.id,
        defaults={"quiz_name": ' '.join([exam_name, str(quiz_number)]),
                  "attempted_date": exam_model['exam_date'],
                  "quiz_type": exam_model['exam_category']}
    )
    if created:
        quiz_score = save_quiz_score(request, exam_model, answer_list)
        quiz_result_obj.quiz_score = quiz_score
        quiz_result_obj.submitted = True
        quiz_result_obj.save()

    response = [{"subject": quiz_result_obj.quiz_name,
                "score": quiz_result_obj.quiz_score}]
    return HttpResponse(json.dumps(
        {'status': 'ok', 'result': response, 'type': 'quiz'}
    ))
