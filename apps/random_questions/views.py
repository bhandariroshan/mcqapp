import random

from django.http import HttpResponse

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi


def generate_random_questions(request):
    '''
    The function generates generates a random question set by randomly picking
    question from all exam sets
    '''
    exammodel_api = ExammodelApi()
    exam_sets = exammodel_api.find_all_exammodel(
        {'exam_family': 'DPS'})
    question_sets = []
    for each_set in exam_sets:
        question_api = QuestionApi()
        questions = question_api.find_all_questions(
            {"exam_code": each_set['exam_code'], 'marks': 1},
            fields={'question_number': 1, '_id': 0, 'exam_code': 1}
        )
        if len(questions) != 0:
            question_sets.append(
                sorted(questions, key=lambda k: k['question_number'])
            )
    final_question_set = []
    if len(question_sets) == 0:
        pass
    elif len(question_sets) == 1:
        final_question_set = question_sets[0]
    else:
        for i in range(len(question_sets[0])):
            final_question_set.append(
                question_sets[random.randrange(len(question_sets))][i]
            )

    return HttpResponse(final_question_set)
