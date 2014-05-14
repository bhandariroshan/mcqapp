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
         "exam_date": 1399998500,
         "image":"exam.jpg", 
         "exam_code" : 100,
         "exam_time" : "7.00pm",
         "exam_category" : "",
         },
        {"exam_name": "IOE model exam 2",
         "exam_date": 1399978500,
         "image":"exam.jpg",         
         "exam_code" : 101,
         "exam_time" : "7.00pm",
         "exam_category" : "",
         },
        {"exam_name": "IOE model exam 3",
         "exam_date": 1399968500,
         "image":"exam.jpg",         
         "exam_code" : 102,
         "exam_time" : "7.00pm",
         "exam_category" : "",
         },
        {"exam_name": "IOE model exam 4",
         "exam_date": 1399968500,
         "image":"exam.jpg",         
         "exam_code" : 103,
         "exam_time" : "7.00pm",
         "exam_category" : ""}
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
    This function receives list of answers and exam_code
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
    for index, choice in enumerate(answer_list):
        if sorted_questions[index]['answer'][choice]['correct'] == 1:
            answer_dict[sorted_questions[index]['subject']] += 1

    total = 0
    for key, value in answer_dict.iteritems():
        total += value
    answer_dict['total'] = total
    return HttpResponse(json.dumps(answer_dict))
