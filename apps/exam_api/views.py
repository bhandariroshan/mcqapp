import json
import datetime

from django.http import HttpResponse

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi


def load_examset_in_database(request):
    '''
    the function is used to load exam set in the exam collection
    of mcq database
    '''
    exam_model = ExammodelApi()
    exam_dict = [
        {"exam_name": "IOE model exam 1",
         "exam_date": datetime.datetime(2014, 5, 20),
         "exam_code": 100},
        {"exam_name": "IOE model exam 2",
         "exam_date": datetime.datetime(2014, 5, 27),
         "exam_code": 200},
        {"exam_name": "IOE model exam 3",
         "exam_date": datetime.datetime(2014, 6, 3),
         "exam_code": 300},
        {"exam_name": "IOE model exam 4",
         "exam_date": datetime.datetime(2014, 6, 10),
         "exam_code": 400}
    ]
    exam_model.insert_new_model(exam_dict)
    return HttpResponse("Exam model saved in the database")


def load_modelquestion_in_database(request):
    '''
    the function is used to load fake data in question collection
    of mcq database in mongodb
    '''
    f = open('apps/exam_api/question_testdata.json', 'rb')

    json_obj = json.loads(f.read())
    for i, x in enumerate(json_obj):
        x['question_number'] = i + 1

    question_api = QuestionApi()
    question_api.insert_new_question(json_obj)
    return HttpResponse("Question saved in the database")


def get_questionset_from_database(request, exam_code):
    '''
    This function returns the questions with same examcode
    '''
    question_api = QuestionApi()
    questions = question_api.find_all({"exam_code": int(exam_code)})
    sorted_questions = sorted(questions, key=lambda k: k['question_number'])
    return HttpResponse(json.dumps(sorted_questions))


def list_exam_set(request):
    '''
    this function lists the available exam models
    '''
    exam_set = ExammodelApi()
    exam_list = exam_set.find_all({})
    return HttpResponse(json.dumps(exam_list))


def check_answers(request, answer_list, exam_code):
    '''
    This function receives dictionary of answers and exam_code
    and return the dictionary with correct answers of each subject
    and sum of correct answers
    '''
    question_api = QuestionApi()
    questions = question_api.find_all({"exam_code": int(exam_code)})
    sorted_questions = sorted(questions, key=lambda k: k['question_number'])
    subjects = set([i['subject'] for i in sorted_questions])
    answer_dict = {}
    for items in subjects:
        answer_dict[items] = 0
    for key, value in answer_list.iteritems():
        for item in sorted_questions:
            if item['question_number'] == int(key):
                if item['answer'][value]['correct'] == 1:
                    answer_dict[item['subject']] += 1
                    break
    total = 0
    for key, value in answer_dict.iteritems():
        total += value
    answer_dict['total'] = total
    return HttpResponse(json.dumps(answer_dict))
