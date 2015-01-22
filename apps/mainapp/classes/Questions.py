from apps.mainapp.classes.MongoConnection import MongoConnection
import time
import datetime

class Question():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'question'
        self.db_object.create_table(self.table_name, '_id')

    def get_questions(self, username, subject):
        if subject == None:
            if username == 'raj':
                questions = self.db_object.get_all(table_name=self.table_name, limit = 25,            
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                        'subject':'physics'})

            if username == 'sujit':
                questions = self.db_object.get_all(self.table_name,  limit = 25,           
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                    'subject':'physics'})

            if username == 'sudip':
                questions = self.db_object.get_all(self.table_name, limit = 25,            
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                    'subject':'chemistry'})

            if username == 'roshan':
                questions = self.db_object.get_all(self.table_name,  limit = 25,           
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                    'subject':'english'})

            if username == 'raj' or username == 'sijan':
                questions = self.db_object.get_all(self.table_name,  limit = 25,           
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                    'subject':'aptitude'})

            if username == 'santosh':
                questions = self.db_object.get_all(self.table_name, limit = 25,            
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                    'subject':'mathematics'})

            if username == "mounteverest":
                questions = self.db_object.get_all(table_name=self.table_name, limit = 25,            
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                    'subject':'botany'})

        else:
            if subject != 'english':
                questions = self.db_object.get_all(table_name=self.table_name, limit = 25,            
                    conditions={'$or':[{'flag_chapter_set':{'$exists':False}},{'difficulty':{'$nin':["1", "2", "3", "4","5"]}}],
                    'subject':subject})
            else:
                questions = self.db_object.get_all(table_name=self.table_name, limit = 300,            
                    conditions={'subject':subject})

        return questions

    def update_question(self, conditions={}, value={}):        
        return self.db_object.update_upsert(self.table_name,conditions,value)


class TopicApi():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'topics'
        self.db_object.create_table(self.table_name, '_id')

    def get_topic(self, conditions={}):
        questions = self.db_object.get_all_vals(self.table_name, 
            conditions=conditions)
        return questions

    def save_topics(self, data={}, conditions={}):
        return self.db_object.update_upsert(self.table_name,conditions,data)