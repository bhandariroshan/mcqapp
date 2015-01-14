from apps.mainapp.classes.MongoConnection import MongoConnection
import time
import datetime

class Question():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'question'
        self.db_object.create_table(self.table_name, '_id')

    def get_questions(self):
        questions = self.db_object.get_all(self.table_name, 
            conditions={'flag_chapter_set':{'$exists':False}, 'subject':'physics'}, limit=30)
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