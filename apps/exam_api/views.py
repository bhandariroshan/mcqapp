from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi,\
    AttemptedAnswerDatabase

from django.http import HttpResponse

class ExamHandler():
    '''
    The class performs activities related to a exam
    '''
    def get_questionset_from_database(self, exam_code):
        '''
        This function returns the questions of a model
        by checking the exam_code
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


def save_user_answers(request):
    '''
    the function receives the information of answer checked by
    user and saved in the answer database
    '''
   

    if request.GET.get('exam_code') is not None:
        answer_dict = {
            "exam_code": request.GET.get('exam_code'),
            "user_id": request.GET.get('user_id'),
            "question_number": request.GET.get('question_number'),
            "answer_choice": request.GET.get('choice')
        }
        attempted_answer = AttemptedAnswerDatabase()
        attempted_answer.insert_new_answer_model(answer_dict)
        print 'Answer Saved in Database'

    else:
        print 'Not a valid method'
