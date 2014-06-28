import random
import datetime
import time

from bson.objectid import ObjectId

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi


def generate_random_ioe_questions(request):
    '''
    The function generates generates a random question set by randomly picking
    question from all exam sets
    '''
    exammodel_api = ExammodelApi()
    exam_sets = exammodel_api.find_all_exammodel(
        {'exam_family': 'DPS', "exam_category": "BE-IOE"})
    question_sets = []
    for each_set in exam_sets:
        question_api = QuestionApi()
        questions = question_api.find_all_questions(
            {"exam_code": each_set['exam_code'], 'marks': 1},
            fields={'question_number': 1}
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
                ObjectId(
                    question_sets[
                        random.randrange(len(question_sets))][i]['uid']['id']
                )
            )
    new_exam_model = {
        "exam_name": "IOE Practice set",
        "exam_date": time.mktime(
            datetime.datetime.now().timetuple()
        ),
        "image": "exam.jpg",
        "exam_code": time.mktime(
            datetime.datetime.now().timetuple()
        ),
        "exam_category": "BE-IOE",
        "exam_duration": 60,
        "exam_family": 'DPS',
        "question_list": final_question_set
    }
    exammodel_api.insert_new_model(new_exam_model)
    print new_exam_model['exam_code']
    return final_question_set
