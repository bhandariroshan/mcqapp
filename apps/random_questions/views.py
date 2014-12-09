import random
import datetime
import time

from bson.objectid import ObjectId
from django.http import HttpResponse

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi


def generate_random_ioe_questions(request):
    '''
    The function generates generates a random question set by randomly picking
    question from all exam sets
    '''
    question_api = QuestionApi()
    distinct_dict = question_api.find_distinct_value('exam_code', {'marks': 1})
    question_sets = []
    for each_code in distinct_dict['results']:
        questions = question_api.find_all_questions(
            {"exam_code": each_code, 'marks': 1},
            fields={'question_number': 1, 'subject': 1}
        )
        if len(questions) == 65:
            question_sets.append(questions)
    final_question_set = []
    if len(question_sets) == 0:
        pass
    elif len(question_sets) == 1:
        final_question_set = question_sets[0]
    else:
        for i in range(len(question_sets[0])):
            if question_sets[0][i]['subject'].lower() != 'english':
                random_num = random.randrange(len(question_sets))

            final_question_set.append(
                ObjectId(
                    question_sets[random_num][i]['uid']['id']
                )
            )

    exammodel_api = ExammodelApi()
    last_exam_code = exammodel_api.find_all_exammodel_descending(
        {},
        fields={"exam_code": 1},
        sort_index="exam_code",
        limit=1
    )
    if len(last_exam_code) > 0:
        new_exam_code = int(last_exam_code[0]['exam_code']) + 1
    else:
        new_exam_code = 1001
    new_exam_model = {
        "exam_name": "IOE Practice set",
        "exam_date": time.mktime(
            datetime.datetime.now().timetuple()
        ),
        "image": "exam.jpg",
        "exam_code": new_exam_code,
        "exam_category": "BE-IOE",
        "exam_duration": 120,
        "exam_family": 'DPS',
        "question_list": final_question_set
    }
    exammodel_api.insert_new_model(new_exam_model)
    return new_exam_code


def add_questions_in_exam_model(request):
    '''
    This function extracts all questions for each exam code and loads
    the list of question id in the exam model
    '''
    exammodel_api = ExammodelApi()
    exam_models = exammodel_api.find_all_exammodel(
        {"question_list": {"$exists": 0}}
    )
    for exams in exam_models:
        question_api = QuestionApi()
        questions = question_api.find_all_questions(
            {"exam_code": exams['exam_code']},
            fields={"_id": 1}
        )
        if len(questions) != 0:
            question_id_list = [ObjectId(i['uid']['id']) for i in questions]
            exammodel_api.update_exam_model(
                {"exam_code": exams['exam_code']},
                {"question_list": question_id_list}
            )
    return HttpResponse('Question list saved in Exam model')


def generate_random_iom_questions(request):
    '''
    The function generates generates a random question set for iom exam by
    randomly picking question from all exam sets
    '''
    question_api = QuestionApi()
    distinct_dict = question_api.find_distinct_value(
        'exam_code',
        {'exam_type': 'MEDICAL'}
    )
    question_sets = []
    for each_code in distinct_dict['results']:
        questions = question_api.find_all_questions(
            {"exam_code": each_code},
            fields={'question_number': 1}
        )
        if len(questions) == 100:
            question_sets.append(questions)
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
    exammodel_api = ExammodelApi()
    last_exam_code = exammodel_api.find_all_exammodel_descending(
        {},
        fields={"exam_code": 1},
        sort_index="exam_code",
        limit=1
    )
    if len(last_exam_code) > 0:
        new_exam_code = int(last_exam_code[0]['exam_code']) + 1
    else:
        new_exam_code = 1001

    new_exam_model = {
        "exam_name": "IOM Practice set",
        "exam_date": time.mktime(
            datetime.datetime.now().timetuple()
        ),
        "image": "exam.jpg",
        "exam_code": new_exam_code,
        "exam_category": "MBBS-IOM",
        "exam_duration": 120,
        "exam_family": 'DPS',
        "question_list": final_question_set
    }
    exammodel_api.insert_new_model(new_exam_model)
    return new_exam_code


def generate_random_moe_questions(request):
    '''
    The function generates generates a random question set for moe exam by
    randomly picking question from each subject
    '''
    exammodel_api = ExammodelApi()
    question_api = QuestionApi()
    subjects = {'physics': 30,
                'chemistry': 30,
                'botany': 20,
                'zoology': 20}
    question_list = []
    for key, value in subjects.iteritems():
        subject_questions = question_api.find_all_questions(
            {"subject": key,
             "exam_type": 'MEDICAL',
             "marks": 1},
            fields={"_id": 1}
        )
        random_list = []
        for i in range(value):
            random_num = random.randrange(len(subject_questions))

            # generate unique random numbers to avoid repetition
            while random_num in random_list:
                random_num = random.randrange(len(subject_questions))
            random_list.append(random_num)
            question_id = subject_questions[random_num]['uid']
            question_list.append(ObjectId(question_id['id']))
    last_exam_code = exammodel_api.find_all_exammodel_descending(
        {},
        fields={"exam_code": 1},
        sort_index="exam_code",
        limit=1
    )
    if len(last_exam_code) > 0:
        new_exam_code = int(last_exam_code[0]['exam_code']) + 1
    else:
        new_exam_code = 1001
    new_exam_model = {
        "exam_name": "MOE Practice set",
        "exam_date": time.mktime(
            datetime.datetime.now().timetuple()
        ),
        "image": "exam.jpg",
        "exam_code": new_exam_code,
        "exam_category": "MBBS-MOE",
        "exam_duration": 120,
        "exam_family": 'DPS',
        "question_list": question_list
    }
    exammodel_api.insert_new_model(new_exam_model)
    return new_exam_code
