from .MongoConnection import MongoConnection


class Notifications():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'notifications'
        self.db_object.create_table(self.table_name, '_id')

    def get_notifications(self):                
        start_time = time.mktime(datetime.date.today().timetuple())
        notices = self.db_object.get_all_vals(self.table_name, {'date':{'$gte':int(start_time)}})
        return notices

    def save_notifications(self, value):
        self.db_object.insert_one(value)

noti = Notifications()        
noti.save_notifications({
    'notification_id':1,
    'message':{
            'title':'Exam Scheduled for today',
            'content':'IOM model exam set is scheduled for today.'
        }
    'status':'ok',
    'date':1401699858
    })