from django.http import HttpResponse

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi


def generate_random_questions():
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
            fields={'answer.correct': 0}
        )
        question_sets.append(
            sorted(questions, key=lambda k: k['question_number'])
        )
    return HttpResponse(question_sets)
