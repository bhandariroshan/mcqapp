from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi,\
    AttemptedAnswerDatabase

from django.http import HttpResponse
import datetime, time
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
        for index, choice in enumerate(answer_list):
            if sorted_questions[index]['answer']['correct'] == choice:
                try:
                    correct_answers[sorted_questions[index]['subject']] += 1
                except:
                    correct_answers[sorted_questions[index]['subject']] = 1
            else:
                try:
                    correct_answers[sorted_questions[index]['subject']] += 0
                except:
                    correct_answers[sorted_questions[index]['subject']] = 0
        total = 0
        score_list = []
        for key, value in correct_answers.iteritems():
            temp = {}
            temp['subject'] = key
            temp['score'] = value
            total += value
            score_list.append(temp)
        score_list.append({'subject': 'Total', 'score': total})
        return score_list


def save_user_answers(request):
    '''
    the function receives the information of answer checked by
    user and saved in the answer database
    '''   
    ans = AttemptedAnswerDatabase()
    question_number = request.POST.get('qid','')
    selected_ans = request.POST.get('sans','')
    exam_code = request.POST.get('exam_code','')
    current_question_number = int(request.POST.get('current_question_number',''))
    attempt_time = datetime.datetime.now()
    attempt_time = time.mktime(attempt_time.timetuple())
    ans.update_upsert_attempted_answer(
        {'q_id':question_number, 'exam_code':exam_code, 'user_id':request.user.id},{
        'user_id':request.user.id,
        'q_id':question_number,
        'exam_code':exam_code,
        'selected_ans':selected_ans,
        'attempt_time':int(attempt_time),
        'q_no':current_question_number
         })
