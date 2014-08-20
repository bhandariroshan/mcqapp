from apps.mainapp.classes.MongoConnection import MongoConnection
import time
import datetime


class ResultRequest():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'SLCresultrequest'
        self.db_object.create_table(self.table_name, 'number')

    def save_result_request_data(self, data):
        start_time = time.mktime(datetime.datetime.now().timetuple())
        data['request_time'] = start_time
        self.db_object.insert_one(self.table_name,data)

class ResultRequestSuccess():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'SLCresultrequestsuccess'
        self.db_object.create_table(self.table_name, 'number')

    def save_result_request_success_data(self, data):
        start_time = time.mktime(datetime.datetime.now().timetuple())
        data['response_time'] = start_time
        self.db_object.insert_one(self.table_name,data)        