'''
this file allows creation and accessing multiple collections
along with multiple databases. For this project it consists of single
database called mcq having collection named question
to save the questions in the database
'''
from apps.mainapp.MongoConnection import MongoConnection


class QuestionApi():

    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'question'
        self.db_object.create_table(self.table_name, 'useruid')

    def insert_new_question(self, value):
        self.db_object.insert_one(self.table_name, value)

    def find_one(self, condition):
        return self.db_object.get_one(self.table_name, condition)

    def find_all(self, condition1):
        return self.db_object.get_all(self.table_name, condition1)

    def update_question(self, where, what):
        return self.db_object.update(self.table_name, where, what)
