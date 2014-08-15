# from django.db import models
import datetime
import time

import mongoengine as mongo


class QuizAnswer(mongo.DynamicDocument):
    '''
    This is the new collection to save quiz answers of the user
    The class uses mongo connect to connect with the mongo database
    '''
    mongo.connect("mcq", host="localhost", port=27017)
    question_id = mongo.ObjectIdField()
    exam_code = mongo.IntField()
    attempted_option = mongo.StringField(max_length=10)
    attempted_date = mongo.IntField(
        default=time.mktime(datetime.datetime.now().date().timetuple())
    )


class QuizResult(mongo.DynamicDocument):
    '''
    The new collection to save user information about the quiz
    '''
    quiz_name = mongo.StringField(max_length=200)
    quiz_code = mongo.IntField()
    attempted_date = mongo.IntField()
    quiz_score = mongo.IntField()
    quiz_type = mongo.StringField(max_length=100)
