from MongoConnection import MongoConnection


class Result():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'result'
        self.db_object.create_table(self.table_name, '_id')

    def save_result(self, result={}):
        self.db_object.update_upsert(self.table_name, result, result)
