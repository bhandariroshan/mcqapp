from .MongoConnection import MongoConnection
import time, datetime
from bson.objectid import ObjectId

class Notifications():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'notifications'
        self.db_object.create_table(self.table_name, '_id')

    def get_notifications(self, user_id):                
        start_time = time.mktime(datetime.date.today().timetuple())
        notices = self.db_object.get_all(table_name=self.table_name, 
            conditions={'to_userid':{'$all':[user_id]}}, fields={'message':1, 'date':1, 'to_userid':1},limit=5)
        for eachNotice in notices:
            to_users = list(eachNotice['to_userid'])
            to_users = to_users.remove(user_id)
            self.update_notices({'_id':ObjectId(eachNotice['uid']['id'])}, {'to_userid':to_users})
        return notices

    def update_notices(self, where, what):
        return self.db_object.update_upsert(self.table_name,where, what)

    def save_notifications(self, value):
        self.db_object.insert_one(self.table_name, value)

noti = Notifications()        
noti.save_notifications({
    'notification_id':1,
    'message':{
            'title':'Exam Scheduled for today',
            'content':'IOM model exam set is scheduled for today.'
        },
    'date':1401699858,
    'to_userid':[1,2,5],
    'sent_userid':[1,2,5]
    })

