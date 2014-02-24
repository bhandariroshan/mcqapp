#!/usr/bin/env python
# encoding: utf-8
from MongoConnection import MongoConnection
from bson.objectid import ObjectId
from bson.code import Code
from bson import BSON
from bson import json_util
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import Connection
from django.conf import settings


class Questions():
    '''This Class contains attributes and methods required to operate on Questions'''
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'questions'
        self.db_object.create_table(self.table_name,'_id')

    def save_question(self, doc):
        return self.db_object.update_upsert(self.table_name,doc,doc)

q = Questions()
q.save_question({})