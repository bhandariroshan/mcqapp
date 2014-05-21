from apps.mainapp.classes.MongoConnection import MongoConnection
import time, datetime

class Schedules():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'schedules'
        self.db_object.create_table(self.table_name,'_id')

    def get_upcoming_schedules(self):
        end_time = time.mktime((datetime.date.today() + datetime.timedelta(30)).timetuple())
        start_time = time.mktime(datetime.date.today().timetuple())
        exams = self.db_object.get_all_vals(self.table_name, {'schedule_date':{'$gte':int(start_time)}, 'schedule_date':{'$lte':int(end_time)}})
        return exams