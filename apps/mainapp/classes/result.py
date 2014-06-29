from MongoConnection import MongoConnection
import time, datetime

class Result():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'result'
        self.db_object.create_table(self.table_name,'_id')
        
    def save_result(self, result={}):
        self.db_object.insert_one(self.table_name, result)