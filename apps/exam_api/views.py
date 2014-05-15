import json

from django.http import HttpResponse

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi


class ExamHandler():
    '''
    The class performs activities related to a exam
    '''
    def get_questionset_from_database(self, exam_code):
        '''
        This function returns the questions with same examcode
        '''
        question_api = QuestionApi()
        questions = question_api.find_all_questions(
            {"exam_code": int(exam_code)})
        sorted_questions = sorted(
            questions, key=lambda k: k['question_number'])
        return sorted_questions

    def list_upcoming_exams(self):
        '''
        this function lists the available exam models
        '''
        exam_set = ExammodelApi()
        exam_list = exam_set.find_all_exammodel({})
        return exam_list

    def check_answers(self, exam_code, answer_list):
        '''
        This function receives list of answers and exam_code
        and return the dictionary with correct answers of each subject
        and sum of correct answers
        '''

        question_api = QuestionApi()
        questions = question_api.find_all_questions(
            {"exam_code": int(exam_code)})
        sorted_questions = sorted(
            questions, key=lambda k: k['question_number'])
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
        return score_list


def get_question_set(self, request, exam_code):
    exam_handler = ExamHandler()
    model_question_set = exam_handler.get_questionset_from_database(
        exam_code)
    return HttpResponse(json.dumps(model_question_set))


def get_upcoming_exams(self, request):
    exam_handler = ExamHandler()
    upcoming_exams = exam_handler.list_upcoming_exams()
    return HttpResponse(json.dumps(upcoming_exams))


def get_scores(self, request):
    exam_code = request.GET.get('exam')
    answer_list = list(request.GET.get('answers'))
    exam_handler = ExamHandler()
    score_dict = exam_handler.check_answers(exam_code, answer_list)
    return HttpResponse(json.dumps(score_dict))
