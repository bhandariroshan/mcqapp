'''
this file allows creation and accessing multiple collections
along with multiple databases. For this project it consists of single
database called mcq having collection named question
to save the questions in the database
'''
from .MongoConnection import MongoConnection


class QuestionApi():

    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'question'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_new_question(self, value):
        self.db_object.insert_one(self.table_name, value)

    def find_one_question(self, condition):
        return self.db_object.get_one(self.table_name, condition)

    def find_all_questions(self, condition1, fields=None):
        return self.db_object.get_all(self.table_name, condition1, fields,
                                      sort_index='question_number', limit=200)

    def update_question(self, where, what):
        return self.db_object.update(self.table_name, where, what)

    def latex_html(self, where, what):
        return self.db_object.update_upsert(self.table_name, where, what)

    def get_count(self, where):
        return self.db_object.get_count(self.table_name, where)

class ExammodelApi():

    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'exammodel'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_new_model(self, value):
        self.db_object.insert_one(self.table_name, value)

    def find_one_exammodel(self, condition):
        return self.db_object.get_one(self.table_name, condition)

    def find_all_exammodel(self, condition1):
        return self.db_object.get_all(self.table_name, condition1)

    def update_exam_model(self, where, what):
        return self.db_object.update(self.table_name, where, what)


class AttemptedAnswerDatabase():

    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'attemptedanswers'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_new_attempted_answer(self, value):
        self.db_object.insert_one(self.table_name, value)

    def find_one_atttempted_answer(self, condition):
        return self.db_object.get_one(self.table_name, condition)

    def find_all_atttempted_answer(self, condition, fields=None, sort_index="q_no"):
        return self.db_object.get_all(self.table_name, condition, fields, sort_index)

    def update_atttempted_answer(self, where, what):
        return self.db_object.update(self.table_name, where, what)

    def update_upsert_push(self, where, what):
        return self.db_object.update_upsert_push(self.table_name, where, what)

    def get_attempted_exams(self, field, where):
        return self.db_object.get_distinct(self.table_name, field, where)
        

class CorrectAnswerDatabase():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'correctanswers'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_new_correct_answer(self, value):
        self.db_object.insert_one(self.table_name, value)

    def find_one_correct_answer(self, condition):
        return self.db_object.get_one(self.table_name, condition)

    def find_all_correct_answer(self, condition1):
        return self.db_object.get_all(self.table_name, condition1)

    def update_correct_answer(self, where, what):
        return self.db_object.update(self.table_name, where, what)

class ExamStartSignal():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'examstartsignal'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_exam_start_signal(self, value):
        self.db_object.update_upsert(self.table_name, value, value)

    def check_exam_started(self, condition):
        return self.db_object.get_one(self.table_name, condition)     

    def update_exam_start_signal(self, where, what):
        return self.db_object.update_upsert(self.table_name, where, what)           

class HonorCodeAcceptSingal():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'honorcodeacceptsingal'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_honor_code_accept_signal(self, value):
        self.db_object.update_upsert(self.table_name, value, value)

    def check_honor_code_accepted(self, condition):
        return self.db_object.get_one(self.table_name, condition)     

    def update_honor_code_accept_Signal(self, where, what):
        return self.db_object.update_upsert(self.table_name, where, what)

class CurrentQuestionNumber():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'currentquestionnumber'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_current_question_number(self, value):
        self.db_object.update_upsert(self.table_name, value, value)

    def check_current_question_number(self, condition):
        return self.db_object.get_one(self.table_name, condition)     

    def update_current_question_number(self, where, what):
        return self.db_object.update_upsert(self.table_name, where, what)