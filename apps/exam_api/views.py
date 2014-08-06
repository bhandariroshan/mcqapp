import datetime
import time
from bson.objectid import ObjectId
import re

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi, AttemptedAnswerDatabase


class ExamHandler():
    '''
    The class performs activities related to a exam
    '''
    sorted_question_list = None
    exam_list = None
    score_list = None

    def get_questionset_from_database(self, exam_code, html=True):
        '''
        This function returns the questions of a model
        by checking the exam_code
        '''
        exammodel_api = ExammodelApi()
        try:
            exam_model = exammodel_api.find_one_exammodel(
                {"exam_code": int(exam_code)}
            )
            question_id_list = [
                ObjectId(i['id']) for i in exam_model['question_list']
            ]
            question_api = QuestionApi()
            if html:
                question_list = question_api.find_all_questions(
                    {
                        '_id': {"$in": question_id_list}
                    },
                    fields={'answer.correct': 0}
                )
            else:
                question_list = question_api.find_all_questions(
                    {
                        '_id': {"$in": question_id_list}
                    },
                    fields={
                        "answer.correct": 0, "question.html": 0,
                        "answer.a.html": 0, "answer.b.html": 0,
                        "answer.c.html": 0, "answer.d.html": 0
                    }
                )
            self.sorted_question_list = sorted(
                question_list, key=lambda k: k['question_number'])
            return True

        except:
            pass

    def get_filtered_question_from_database(self, exam_code, subject_name):
        '''
        This function returns the questions of a model
        by checking the exam_code
        '''
        exammodel_api = ExammodelApi()
        try:
            exam_model = exammodel_api.find_one_exammodel(
                {"exam_code": int(exam_code)}
            )
            question_id_list = [
                ObjectId(i['id']) for i in exam_model['question_list']
            ]

            question_api = QuestionApi()
            question_list = question_api.find_all_questions({
                '_id': {"$in": question_id_list},
                'subject': {"$regex": re.compile(
                    "^" + str(subject_name) + "$", re.IGNORECASE),
                    "$options": "-i"},
            })
            sorted_questions = sorted(
                question_list, key=lambda k: k['question_number'])
            return sorted_questions

        except:
            pass

    def get_paginated_question_set(self, exam_code, current_pg_num):
        exammodel_api = ExammodelApi()
        exam_model = exammodel_api.find_one_exammodel(
            {"exam_code": int(exam_code)}
        )
        questions_list = exam_model['question_list']
        question_id_list = [
            ObjectId(i['id']) for i in questions_list
        ]
        question_api = QuestionApi()
        return_question_list = question_api.get_paginated_questions(
            {'_id': {"$in": question_id_list}},
            fields={'answer.correct': 0},
            page_num=current_pg_num
        )
        return return_question_list

    def list_upcoming_exams(self, condition={}, fields=None):
        '''
        this function lists the available exam models
        '''
        exam_set = ExammodelApi()
        exam_list = exam_set.find_all_exammodel(condition, fields=fields)
        for eachExam in exam_list:
            eachExam['exam_code'] = int(eachExam['exam_code'])
            eachExam['exam_date'] = int(eachExam['exam_date'])
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
        question_id_list = [
            ObjectId(i['id']) for i in exam_model['question_list']
        ]
        question_api = QuestionApi()
        question_list = question_api.find_all_questions(
            {
                '_id': {"$in": question_id_list},
            }
        )
        sorted_questions = sorted(
            question_list, key=lambda k: k['question_number'])

        negative_marking = False
        if exam_model['exam_category'] == "BE-IOE" and sorted_questions[0]['marks'] == 1:
            negative_marking = True

        subjects = set([i['subject'].lower() for i in sorted_questions])

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
                sorted_questions[index]['subject'].lower()][
                'subject_total_marks'] += 1 * int(sorted_questions[index]['marks'])

            if choice in ['a', 'b', 'c', 'd']:
                correct_answers[
                    sorted_questions[index][
                        'subject'].lower()]['attempted'] += 1
                if sorted_questions[index]['answer']['correct'] == choice:
                    try:
                        correct_answers[sorted_questions[index][
                            'subject'].lower()]['correct_subject_answer'] += 1
                        correct_answers[sorted_questions[index][
                            'subject'].lower()]['score'] += 1 * int(sorted_questions[index]['marks'])
                    except:
                        correct_answers[
                            sorted_questions[index]['subject'].lower()]['score'] += 1
                elif negative_marking:
                    try:
                        correct_answers[
                            sorted_questions[index]['subject'].lower()]['score'] -= 0.25
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
