from MongoConnection import MongoConnection
import time, datetime

class UserProfile():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'_id')

    def save_user(self, user={}):
        self.db_object.insert_one(self.table_name, user)

    def get_user_by_username(self, user_name=''):
        return self.db_object.get_one(self.table_name,{'username':user_name})

    def update_upsert(self, where={}, what={}):
        return self.db_object.update_upsert(self.table_name, where, what)

    def check_subscription_plan(self, user_name):
        user = self.db_object.get_one(self.table_name, {'username':user_name})
        if user != None:
            if user['subscription_type'] == 'IDP':
                return {'status':'ok', 'subscription_type':'IDP'}
            elif user['subscription_type'] == 'BE-IOE-071':
                return {'status':'ok', 'subscription_type':'BE-IOE-071'}
            elif user['subscription_type'] == 'MBBS-IOM-071':
                return {'status':'ok', 'subscription_type':'MBBS-IOM-071'}
            else:                
                return {'status':'error', 'message':'no subscription plan associated'}
        else:
            return {'status':'error', 'message':'Invalid Request'}

    def check_subscription_by_exam_id(self, user_name, exam_code):
        user = self.db_object.get_one(self.table_name, {'username':user_name})
        valid_exams = user['valid_exam']
        if exam_code in valid_exams:
            return True
        else:
            return False

    def get_subscribed_exams(self, user_name=''):
        user = self.db_object.get_one(self.table_name, {'username':user_name})
        valid_exams = user['valid_exam']
        return valid_exams

    def get_subscription_plan(self, user_name=''):
        user = self.db_object.get_one(self.table_name, {'username':user_name})
        subscription_type = user['subscription_type']
        return subscription_type

    def check_subscribed(self, user_name, exam_code):
        user = self.db_object.get_one(self.table_name, {'username':user_name})
        exam_obj = ExammodelApi()
        exam_details = exam_obj.find_one_exammodel({'exam_code':int(exam_code)})            
        if user != None:
            if user['subscription_type'] == 'IDP':
                return True                    
            elif exam_details['exam_category'] == user['subscription_type']:
                return True
            else:
                subscribed_exams = self.get_subscribed_exams(user_name)
                if exam_code in subscribed_exams:
                    return True
                else:
                    return False
        else:
            return False