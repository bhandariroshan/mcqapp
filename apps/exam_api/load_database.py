import json
from bson.objectid import ObjectId
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi,\
    CorrectAnswerDatabase
from django.conf import settings


@user_passes_test(lambda u: u.is_superuser)
def load_examset_in_database(request):
    '''
    the function is used to load fake exam set in the exam collection
    of mcq database
    '''
    question_api = QuestionApi()
    distinct_dict = question_api.find_distinct_value('exam_code', {})
    exam_list = []
    for dist in distinct_dict['results']:
        questions = question_api.find_all_questions(
            {"exam_code": dist}, fields={"_id": 1}
        )
        if len(questions) != 0:
            question_id_list = [ObjectId(i['uid']['id']) for i in questions]
            exam_dict = {
                "exam_name": "IOE Practice Exam",
                "exam_date": 1401359880,
                "image": "exam.jpg",
                "exam_code": dist,
                "exam_category": "BE-IOE",
                "exam_duration": 60,
                "exam_family": 'DPS',
                "question_list": question_id_list
            }
            exam_list.append(exam_dict)
    exam_model = ExammodelApi()
    # exam_dict = [
    #     {"exam_name": "IOE Practice Exam 1",
    #      "exam_date": 1401359880,
    #      "image": "exam.jpg",
    #      "exam_code": 201,
    #      "exam_category": "BE-IOE",
    #      "exam_duration": 60,
    #      "exam_family": 'DPS'
    #      },
    #     {"exam_name": "IOM Model Exam 1",
    #      "exam_date": 1403916646,
    #      "exam_time": "1.00pm",
    #      "image": "exam.jpg",
    #      "exam_code": 101,
    #      "exam_category": "MBBS-IOM",
    #      "exam_duration": 180,
    #      "exam_family": 'CPS'
    #      },
    #     {"exam_name": "IOE Model Exam 1",
    #      # "exam_date": 1401258859,
    #      "exam_date": 1403612147,
    #      "image": "exam.jpg",
    #      "exam_code": 204,
    #      "exam_time": "1.00pm",
    #      "exam_duration": 60,
    #      "exam_category": "BE-IOE",
    #      "exam_family": 'CPS'
    #      },
    #     {"exam_name": "IOE Practice Exam 2",
    #      "exam_date": 1399978500,
    #      "image": "exam.jpg",
    #      "exam_code": 202,
    #      "exam_category": "BE-IOE",
    #      "exam_duration": 60,
    #      "exam_family": 'DPS'
    #      },
    #     {"exam_name": "IOE Practice Exam 3",
    #      "exam_date": 1399978500,
    #      "image": "exam.jpg",
    #      "exam_code": 203,
    #      "exam_category": "BE-IOE",
    #      "exam_duration": 60,
    #      "exam_family": 'DPS'
    #      },
    #     {"exam_name": "IOE Practice Exam 4",
    #      "exam_date": 1403612147,
    #      "image": "exam.jpg",
    #      "exam_code": 205,
    #      "exam_category": "BE-IOE",
    #      "exam_duration": 60,
    #      "exam_family": 'DPS'
    #      },
    #     {"exam_name": "IOM Practice Exam 1",
    #      "exam_date": 1403912850,
    #      "image": "exam.jpg",
    #      "exam_code": 301,
    #      "exam_category": "MBBS-IOM",
    #      "exam_duration": 120,
    #      "exam_family": 'DPS'
    #      },
    #     {"exam_name": "IOM Practice Exam 2",
    #      "exam_date": 1403912850,
    #      "image": "exam.jpg",
    #      "exam_code": 302,
    #      "exam_category": "MBBS-IOM",
    #      "exam_duration": 120,
    #      "exam_family": 'DPS'
    #      }
    # ]
    exam_model.insert_new_model(exam_list)
    return HttpResponse("Exam model saved in the database")


@user_passes_test(lambda u: u.is_superuser)
def load_modelquestion_in_database(request):
    '''
    the function is used to load fake data in question collection
    of mcq database in mongodb
    '''
    for var in range(201, 206):
        f = open('apps/exam_api/' + str(var) + '.json', 'rb')
        json_obj = json.loads(f.read())
        for i, x in enumerate(json_obj):
            x['question_number'] = i + 1
        question_api = QuestionApi()
        question_api.insert_new_question(json_obj)

    for var in range(301, 303):
        f = open('apps/exam_api/' + str(var) + '.json', 'rb')
        json_obj = json.loads(f.read())
        for i, x in enumerate(json_obj):
            x['question_number'] = i + 1
        question_api = QuestionApi()
        question_api.insert_new_question(json_obj)

    for var in range(1, 11):
        if var == 6:
            continue
        f = open(settings.APP_ROOT + '/apps/exam_api/extraction/v4s' +
                 str(var) + '/text.docx-json.json-new_json.json', 'rb')
        json_obj = json.loads(f.read())
        for i, x in enumerate(json_obj):
            x['question_number'] = i + 1
        question_api = QuestionApi()
        question_api.insert_new_question(json_obj)
    return HttpResponse("Question saved in the database")


def load_correctanswer_in_database(request):
    '''
    This function loads the correct answers of each question in the database
    Each document consists of question_id and correct answer choice
    '''
    question_api = QuestionApi()
    questions = question_api.find_all_questions(
        {"exam_code": 103})
    correct_answer_list = []
    for each_question in questions:
        temp = {}
        temp['question_id'] = ObjectId(each_question['uid']['id'])
        temp['correct_answer'] = each_question['answer']['correct']
        correct_answer_list.append(temp)
    correct_answer_database = CorrectAnswerDatabase()
    correct_answer_database.insert_new_correct_answer(correct_answer_list)
    return HttpResponse("Correct Answer saved in the database")
