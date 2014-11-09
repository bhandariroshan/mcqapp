from MongoConnection import MongoConnection
from apps.mainapp.classes.query_database import ExammodelApi
from apps.random_questions.views import generate_random_ioe_questions, generate_random_iom_questions
from apps.mainapp.classes.Coupon import Coupon
import time, datetime

class UserProfile():
    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'userprofile'
        # self.db_object.create_table(self.table_name)

    def search_user(self, query):
        return self.db_object.get_all(
            self.table_name,
            {
                '$or': [
                    {'username': {'$regex': "(?i).*" + query + ".*"}},
                    {'email': {'$regex': "(?i).*" + query + ".*"}},
                    {'name': {'$regex': "(?i).*" + query + ".*"}}
                ]
            }
        )

    def get_all_users(self, limit=200):
        return self.db_object.get_all(self.table_name, limit=limit)

    def save_user(self, user={}):
        self.db_object.insert_one(self.table_name, user)

    def get_user_by_username(self, user_name=''):
        return self.db_object.get_one(self.table_name, {'username': user_name})

    def get_user_by_userid(self, useruid=''):
        return self.db_object.get_one(self.table_name, {'useruid': useruid})

    def update_profile_image(self, profile_image, username):
        return self.db_object.update(
            self.table_name,
            {'username': username},
            {'profile_image': profile_image}
        )

    def update_upsert(self, where={}, what={}):
        return self.db_object.update_upsert(self.table_name, where, what)

    def update_push(self, where={}, what={}):
        return self.db_object.update_push(self.table_name, where, what)

    def check_subscription_plan(self, user_name):
        user = self.db_object.get_one(self.table_name, {'username': user_name})
        if user is not None:
            if user['subscription_type'] == 'IDP':
                return {'status': 'ok', 'subscription_type': 'IDP'}
            elif user['subscription_type'] == 'BE-IOE':
                return {'status': 'ok', 'subscription_type': 'BE-IOE'}
            elif user['subscription_type'] == 'MBBS-IOM':
                return {'status': 'ok', 'subscription_type': 'MBBS-IOM'}
            else:
                return {'status': 'error',
                        'message': 'no subscription plan associated'}
        else:
            return {'status': 'error', 'message': 'Invalid Request'}

    def check_subscription_by_exam_id(self, user_name, exam_code):
        user = self.db_object.get_one(self.table_name, {'username': user_name})
        valid_exams = user['valid_exam']
        if exam_code in valid_exams:
            return True
        else:
            return False

    def get_subscribed_exams(self, user_name=''):
        user = self.db_object.get_one(self.table_name, {'username': user_name})
        valid_exams = user['valid_exam']
        return valid_exams

    def get_subscription_plan(self, user_name=''):
        user = self.db_object.get_one(self.table_name, {'username': user_name})
        subscription_type = user['subscription_type']
        return subscription_type

    def change_subscription_plan(self, user_name, coupon_code):
        coupon_obj = Coupon()
        coupon = coupon_obj.get_coupon_by_coupon_code(coupon_code)
        user = self.db_object.get_one(self.table_name, {'username': user_name})
        subscription_type = list(user['subscription_type'])
        if coupon['subscription_type'] not in subscription_type and \
                coupon['subscription_type'] not in ['DPS', 'CPS']:
            subscription_type.append(coupon['subscription_type'])

        current_time = time.mktime(datetime.datetime.now().timetuple())
        
        return self.db_object.update_upsert(
            self.table_name,
            {'username': user_name},
            {'subscription_type': subscription_type, 'subscribed_date':current_time}
        )

    def check_subscribed(self, user_name, exam_code):
        user = self.db_object.get_one(self.table_name, {'username': user_name})
        exam_obj = ExammodelApi()
        exam_details = exam_obj.find_one_exammodel(
            {'exam_code': int(exam_code)}
        )
        if user is not None:
            if 'IDP' in user['subscription_type']:
                return True
            elif exam_details['exam_category'] in user['subscription_type']:
                return True
            else:
                subscribed_exams = self.get_subscribed_exams(user_name)
                if int(exam_code) in subscribed_exams:
                    return True
                else:
                    return False
        else:
            return False

    def save_coupon(self, username, coupon_code):
        user = self.db_object.get_one(self.table_name, {'username': username})
        coupons = list(user['coupons'])
        if coupon_code not in coupons:
            coupons.append(coupon_code)
        return self.db_object.update_upsert(
            self.table_name,
            {'username': username},
            {'coupons': coupons}
        )

    def save_valid_exam(self, username, exam_code):
        user = self.db_object.get_one(self.table_name, {'username': username})
        valid_exam = list(user['valid_exam'])
        if exam_code not in valid_exam:
            valid_exam.append(int(exam_code))
        return self.db_object.update_upsert(
            self.table_name,
            {'username': username},
            {'valid_exam': valid_exam}
        )

    def save_valid_subject_exam(self, username, subject_exam_code, subject_name):
        user = self.db_object.get_one(self.table_name, {'username': username})
        
        try:
            valid_subject_exam = list(user['valid_subject_exam'])
        except:
            valid_subject_exam = []

        valid_subject_exam_codes = []

        for eachValidExam in valid_subject_exam:
            valid_subject_exam_codes.append(eachValidExam['exam_code'])

        request_time = datetime.datetime.now()
        gen_time = time.mktime(request_time.timetuple())
        if subject_exam_code not in valid_subject_exam_codes:
            valid_subject_exam.append({'exam_category':str(subject_name).lower() +'-test','exam_code':int(subject_exam_code), 'added_time':gen_time})


        return self.db_object.update_upsert(
            self.table_name,
            {'username': username},
            {'valid_subject_exam': valid_subject_exam}
        )

    def save_valid_practice_exam(self, username, practice_exam_code, ex_type):
        user = self.db_object.get_one(self.table_name, {'username': username})
        
        try:
            valid_practice_exam = list(user['valid_practice_exam'])
        except:
            valid_practice_exam = []

        valid_practice_exam_codes = []

        for eachValidExam in valid_practice_exam:
            valid_practice_exam_codes.append(eachValidExam['exam_code'])

        request_time = datetime.datetime.now()
        gen_time = time.mktime(request_time.timetuple())
        if practice_exam_code not in valid_practice_exam_codes:
            valid_practice_exam.append({'exam_category':ex_type, 'exam_code':int(practice_exam_code), 'exam_family':'DPS', 'added_time':gen_time})

        return self.db_object.update_upsert(
            self.table_name,
            {'username': username},
            {'valid_practice_exam': valid_practice_exam}
        )
        

    def get_user_by_coupon(self, coupon_code):
        return self.db_object.get_one(
            self.table_name, {'coupons': coupon_code}
        )

    def check_generate_and_save_valid_exam(self, ex_type, username, request):
        user = self.get_user_by_username(username)
        exam_model_api_obj = ExammodelApi()
        exam_codes = exam_model_api_obj.find_all_exam_codes(condition={'exam_category':ex_type.upper()})
        subscription_type = self.get_subscription_plan(username)

        if 'IDP' not in subscription_type and 'BE-IOE' not in subscription_type and 'MBBS-IOM' not in subscription_type:
            ''' This section is for general  user. '''
            try:
                valid_practice_exam = list(user['valid_practice_exam'])
            except:
                valid_practice_exam = []
            if len(valid_practice_exam) > 0:
                return {'status':'error', 'message':'General user can attempt only one exam for free. However you can attempt free quizes and other subject test. '}
            else:
                for eachExamCode in exam_codes:
                    if eachExamCode not in user['valid_exam']:
                        self.save_valid_exam(username, int(eachExamCode))    
                        self.save_valid_practice_exam(username, eachExamCode, ex_type)
                        return {'status':'ok', 'exam_code':eachExamCode}

                if ex_type == 'be-ioe':
                    exam_code = generate_random_ioe_questions(request)
                elif ex_type == 'mbbs-iom':
                    exam_code = generate_random_iom_questions(request)
                self.save_valid_exam(username, int(exam_code))
                self.save_valid_practice_exam(username, exam_code, ex_type)
                return {'status':'ok', 'exam_code':exam_code}

        elif 'IDP' in subscription_type or 'BE-IOE' in subscription_type or 'MBBS-IOM' in subscription_type:            
            ''' This section is for premium  user. '''
            if ex_type.upper() in subscription_type:
                for eachExamCode in exam_codes:
                        if eachExamCode not in user['valid_exam']:
                            self.save_valid_exam(username, int(eachExamCode))    
                            self.save_valid_practice_exam(username, eachExamCode, ex_type)
                            return {'status':'ok', 'exam_code':eachExamCode}
                        
                if ex_type == 'be-ioe':
                    exam_code = generate_random_ioe_questions(request)
                elif ex_type == 'mbbs-iom':
                    exam_code = generate_random_iom_questions(request)
                self.save_valid_exam(username, int(exam_code))
                self.save_valid_practice_exam(username, exam_code, ex_type)
                return {'status':'ok', 'exam_code':exam_code}
            else:
                return {'status':'error', 'message':'Premium users can attend only one exam related to other category.'}

        

    def check_generate_and_save_valid_subject_exam(self, username, subject_name):
        '''
            This method checks:
                a. If the user is general user then he/she has already given subject exam or not.
                    If he has given then doesn't generate new exam else generates new exam.
                b. If the user is premium user then generate new subject exam. 
        '''
        from apps.testapp.views import generate_random_subject_test
        user = self.db_object.get_one(self.table_name, {'username': username})        
        subscription_type = self.get_subscription_plan(username)
        
        exam_model_api_obj = ExammodelApi()

        if 'IDP' not in subscription_type and 'BE-IOE' not in subscription_type and 'MBBS-IOM' not in subscription_type:
            try:
                valid_subject_exam = list(user['valid_subject_exam'])
            except:
                valid_subject_exam = []

            subject_list = []
            for eachValidExam in valid_subject_exam:
                subject_list.append(eachValidExam['exam_category'])

            if len(valid_subject_exam) > 0 and (str(subject_name.lower()) + '-test' in subject_list) :
                return {'status':'error', 'message':'General user can attempt only one exam for free. However you can attempt free quizes and other subject test. '}
            else:
                exam_codes = exam_model_api_obj.find_all_exam_codes(condition={'exam_category':subject_name.lower()+'-test'})
                for eachExamCode in exam_codes:
                    if eachExamCode not in user['valid_exam']:
                        self.save_valid_exam(username, int(eachExamCode))    
                        self.save_valid_subject_exam(
                            username, eachExamCode, subject_name
                        )
                        return {'status':'ok', 'exam_code':eachExamCode}

                subject_test_exam_code = generate_random_subject_test(str(subject_name))
                self.save_valid_exam(username, int(eachExamCode))    
                self.save_valid_subject_exam(
                    username, eachExamCode, subject_name
                )                
                return {'status':'ok', 'exam_code':subject_test_exam_code}

        elif 'IDP' in subscription_type or 'BE-IOE' in subscription_type or 'MBBS-IOM' in subscription_type:
            exam_codes = exam_model_api_obj.find_all_exam_codes(condition={'exam_category':subject_name.lower()+'-test'})
            for eachExamCode in exam_codes:
                if eachExamCode not in user['valid_exam']:
                    self.save_valid_exam(username, int(eachExamCode))    
                    self.save_valid_subject_exam(
                        username, eachExamCode, subject_name
                    )
                    return {'status':'ok', 'exam_code':eachExamCode}  
                                          
            subject_test_exam_code = generate_random_subject_test(str(subject_name))
            self.save_valid_exam(username, int(eachExamCode))    
            self.save_valid_subject_exam(
                username, eachExamCode, subject_name
            )                
            return {'status':'ok', 'exam_code':subject_test_exam_code}