import datetime
import time
from bson.objectid import ObjectId
import re

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi, AttemptedAnswerDatabase
from apps.mainapp.classes.result import Result


class ExamHandler():
    '''
    The class performs activities related to a exam
    '''
    sorted_question_list = None
    exam_list = None
    user_exam_result = None

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
                        "answer.correct":0, "question.html": 0,
                        "answer.a.html": 0, "answer.b.html": 0,
                        "answer.c.html": 0, "answer.d.html": 0
                    },
                    sort_index='question_number'
                )
            self.sorted_question_list = question_list
            return True

        except:
            return False

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
            question_list = question_api.find_all_questions(
                {'_id': {"$in": question_id_list},
                 'subject': {"$regex": re.compile(
                     "^" + str(subject_name) + "$", re.IGNORECASE),
                     "$options": "-i"},
                 },
                fields=None,
                sort_index='question_number'
            )
            self.sorted_question_list = question_list
            return True

        except:
            return False

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
            sort_index='question_number',
            page_num=current_pg_num
        )
        self.sorted_question_list = return_question_list
        return True

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

    def save_exam_result(self, request, exam_model, ess_time):
        '''
        This function receives exam_code, user_id and ess_time and
        saves the result of each subject of the exam in the result
        collection
        '''
        exam_code = exam_model['exam_code']
        question_id_list = [
            ObjectId(i['id']) for i in exam_model['question_list']
        ]
        question_api = QuestionApi()
        sorted_questions = question_api.find_all_questions(
            {'_id': {"$in": question_id_list}},
            sort_index='question_number'
        )

        # negative marking for 1 marks pulchowk exam.
        negative_marking = False
        if exam_model['exam_category'] in ["BE-IOE", "MBBS-MOE"] and sorted_questions[0]['marks'] == 1:
            negative_marking = True

        subjects = set([i['subject'].lower() for i in sorted_questions])

        correct_answers = {}
        for subs in subjects:
            temp = {}
            temp['subject_total_marks'] = 0
            temp['correct_subject_answer_count'] = 0
            temp['attempted'] = 0
            temp['subject_score'] = 0
            correct_answers[subs] = temp

        # find all answers given by users of this exam
        answer_database = AttemptedAnswerDatabase()
        all_ans = answer_database.find_all_atttempted_answer({
            'exam_code': int(exam_code),
            'user_id': request.user.id,
            'ess_time': ess_time
        },
            fields={'q_id': 1, 'attempt_details': 1}
        )

        # the dictionary saves the question attempted by the user with
        # the option chosen
        attempted_ans_dict = {}
        for ans in all_ans:
            attempted_ans_dict[ans['quid']] = ans['attempt_details'][-1]['selected_ans']

        # calculate score obtained in each subject
        for ques in sorted_questions:
            correct_answers[ques['subject'].lower()][
                'subject_total_marks'] += int(ques['marks'])
            try:
                option = attempted_ans_dict[ques['uid']['id']]
            except:
                option = 'e'
            if option in ['a', 'b', 'c', 'd']:
                correct_answers[ques['subject'].lower()]['attempted'] += 1
                if option == ques['answer']['correct']:
                    correct_answers[ques['subject'].lower()]['correct_subject_answer_count'] += 1
                    correct_answers[ques['subject'].lower()]['subject_score'] += int(ques['marks'])
                elif negative_marking:
                    correct_answers[ques['subject'].lower()]['subject_score'] -= 0.25

        total_score = 0
        total_attempted = 0
        total_marks = 0
        total_correct_answers = 0
        score_list = []

        # saves the score of each subject in the result collection along
        # with user_id, exam_code, ess_time and the score
        result_obj = Result()
        for key, value in correct_answers.iteritems():
            temp = {}
            temp['subject'] = key
            temp['score'] = value['subject_score']
            temp['attempted'] = value['attempted']
            temp['subject_total_marks'] = value['subject_total_marks']
            temp['correct_subject_answer'] = value['correct_subject_answer_count']
            result_obj.save_result({
                'useruid': request.user.id,
                'exam_code': int(exam_code),
                'ess_time': ess_time,
                'result': temp
            })
            score_list.append(temp)
            total_score += value['subject_score']
            total_attempted += value['attempted']
            total_marks += value['subject_total_marks']
            total_correct_answers += value['correct_subject_answer_count']

        total_dict = {
            'subject': 'Total',
            'score': total_score,
            'attempted': total_attempted,
            'subject_total_marks': total_marks,
            'correct_subject_answer': total_correct_answers
        }
        score_list.append(total_dict)
        result_obj.save_result({
            'useruid': request.user.id,
            'exam_code': int(exam_code),
            'ess_time': ess_time,
            'result': total_dict
        })
        self.user_exam_result = score_list
        return True


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
