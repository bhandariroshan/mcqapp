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


def get_questionset_from_database(request, exam_code, web_reponse=0):
    '''
    This function returns the questions with same examcode
    '''
    question_api = QuestionApi()
    questions = question_api.find_all({"exam_code": int(exam_code)})
    sorted_questions = sorted(questions, key=lambda k: k['question_number'])
    if web_reponse == 0:
        return HttpResponse(json.dumps(sorted_questions))
    else:
        return sorted_questions


def list_exam_set(request, web_reponse=0):
    '''
    this function lists the available exam models
    '''
    exam_set = ExammodelApi()
    exam_list = exam_set.find_all({})
    if web_reponse == 0:
        return HttpResponse(json.dumps(exam_list))
    else:
        return exam_list


def check_answers(request, web_reponse=0):
    '''
    This function receives list of answers and exam_code
    and return the dictionary with correct answers of each subject
    and sum of correct answers
    '''
    exam_code = request.GET.get('exam')
    answer_list = list(request.GET.get('answers'))
    print 'answer_list', len(answer_list)
    question_api = QuestionApi()
    questions = question_api.find_all({"exam_code": int(exam_code)})
    sorted_questions = sorted(questions, key=lambda k: k['question_number'])
    correct_answers = {}
    for index, choice in enumerate(answer_list):
        if sorted_questions[index]['answer']['correct'] == choice:
            try:
                correct_answers[sorted_questions[index]['subject']] += 1
            except:
                correct_answers[sorted_questions[index]['subject']] = 1
    total = 0
    score_list = []
    for key, value in correct_answers.iteritems():
        temp = {}
        temp['subject'] = key
        temp['score'] = value
        total += value
        score_list.append(temp)
    score_list.append({'subject': 'total', 'score': total})

    if web_reponse == 0:
        return HttpResponse(json.dumps(score_list))
    else:
        return score_list
