# from django.db import models
import datetime

import mongoengine as mongo


# Create your models here.


class QuizAnswer(mongo.DynamicDocument):
    '''
    This is the new collection to save quiz answers of the user
    The class uses mongo connect to connect with the mongo database
    '''
    mongo.connect("mcq", host="localhost", port=27017)
    question_id = mongo.ObjectIdField()
    attempted_option = mongo.StringField(max_length=10)
    created_date = mongo.StringField(default=str(datetime.datetime.utcnow().date()))
