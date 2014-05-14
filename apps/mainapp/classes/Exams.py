from apps.mainapp.classes.MongoConnection import MongoConnection
import time, datetime

class Exam():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'exammodel'
        self.db_object.create_table(self.table_name,'_id')

    def get_upcoming_exams(self):    	
    	end_time = time.mktime((datetime.date.today() + datetime.timedelta(7)).timetuple())
    	start_time = time.mktime(datetime.date.today().timetuple())
    	exams = self.db_object.get_all_vals(self.table_name, {'exam_date':{'$gte':int(start_time)}, 'exam_date':{'$lte':int(end_time)}})
    	return exams

    def get_exam_detail(self, exam_code):
        return self.db_object.get_one(self.table_name, {'exam_code':exam_code})

class RankCard():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcqapp')
        self.table_name = 'rankcard'
        self.db_object.create_table(self.table_name,'_id')

    def get_rank_card(self, useruid, exam_code):
        rankcard = self.db_object.get_all_vals(self.table_name, 
            {'exam_code':exam_code, 'useruid':useruid})
        return rankcard

class ScoreCard():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcqapp')
        self.table_name = 'scorecard'
        self.db_object.create_table(self.table_name,'_id')

    def get_score_card(self, useruid, exam_code):
        rankcard = self.db_object.get_all_vals(self.table_name, 
            {'exam_code':exam_code, 'useruid':useruid})
        return rankcard


