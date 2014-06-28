from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi,\
    AttemptedAnswerDatabase

import datetime
import time


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
            {"exam_code": int(exam_code), 'marks':1})
        sorted_questions = sorted(
            questions, key=lambda k: k['question_number'])
        return sorted_questions

    def list_upcoming_exams(self, condition={}):
        '''
        this function lists the available exam models
        '''
        exam_set = ExammodelApi()
        exam_list = exam_set.find_all_exammodel(condition)
        return exam_list

    def check_answers(self, exam_code, answer_list):
        '''
        This function receives list of answers and exam_code
        and return the dictionary with correct answers of each subject
        and sum of correct answers
        '''
        exammodel_api = ExammodelApi()
        exam_model = exammodel_api.find_one_exammodel(
            {'exam_code': int(exam_code)}
        )
        question_api = QuestionApi()
        questions = question_api.find_all_questions(
            {"exam_code": int(exam_code), 'marks':1})
        sorted_questions = sorted(
            questions, key=lambda k: k['question_number'])
        subjects = set([i['subject'] for i in sorted_questions])

        correct_answers = {}
        for subs in subjects:
            temp = {}
            temp['subject_total_marks'] = 0
            temp['correct_subject_answer'] = 0
            temp['attempted'] = 0
            temp['score'] = 0
            correct_answers[subs] = temp

        for index, choice in enumerate(answer_list):
            correct_answers[
                sorted_questions[index]['subject']]['subject_total_marks'] += \
                1 * int(sorted_questions[index]['marks'])
            if choice in ['a', 'b', 'c', 'd']:
                correct_answers[
                    sorted_questions[index]['subject']]['attempted'] += 1
                if sorted_questions[index]['answer']['correct'] == choice:
                    try:
                        correct_answers[sorted_questions[index]['subject']][
                            'correct_subject_answer'
                        ] += 1
                        correct_answers[sorted_questions[index]['subject']][
                            'score'
                        ] += 1 * int(sorted_questions[index]['marks'])
                    except:
                        correct_answers[
                            sorted_questions[index]['subject']][
                            'score'
                        ] += 1
                else:
                    if exam_model['exam_category'] in ["BE-IOE", "MBBS-MOE"]:
                        try:
                            correct_answers[
                                sorted_questions[index]['subject']
                            ]['score'] -= 0.25
                        except:
                            pass

        total_score = 0
        total_attempted = 0
        total_marks = 0
        total_correct_answers = 0
        score_list = []

        for key, value in correct_answers.iteritems():
            temp = {}
            temp['subject'] = key
            temp['score'] = value['score']
            temp['attempted'] = value['attempted']
            temp['subject_total_marks'] = value['subject_total_marks']
            temp['correct_subject_answer'] = value['correct_subject_answer']
            total_score += value['score']
            total_attempted += value['attempted']
            total_marks += value['subject_total_marks']
            total_correct_answers += value['correct_subject_answer']
            score_list.append(temp)
        score_list.append(
            {
                'subject': 'Total',
                'score': total_score,
                'attempted': total_attempted,
                'correct_subject_answer': total_correct_answers,
                'subject_total_marks': total_marks
            }
        )
        return score_list


def save_user_answers(request, ess_starttimestamp):
    '''
    the function receives the information of answer checked by
    user and saved in the answer database
    '''
    ans = AttemptedAnswerDatabase()
    question_number = request.POST.get('qid', '')
    selected_ans = request.POST.get('sans', '')
    exam_code = request.POST.get('exam_code', '')
    current_question_number = int(request.POST.get(
        'current_question_number', ''))
    attempt_time = datetime.datetime.now()
    attempt_time = time.mktime(attempt_time.timetuple())
    ans.update_upsert_push({
        'user_id': request.user.id,
        'ess_time': int(ess_starttimestamp),
        'q_id': question_number,
        'exam_code': int(exam_code),
        'q_no': current_question_number}, {
        'attempt_details': {
            'selected_ans': selected_ans,
            'attempt_time': int(attempt_time)
        }})
