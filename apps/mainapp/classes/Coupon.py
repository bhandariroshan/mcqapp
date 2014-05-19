from MongoConnection import MongoConnection
import time, datetime

class Coupon():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'coupons'
        self.db_object.create_table(self.table_name,'_id')
        
    def generate_coupons(self, subscription_type):
    	'''
    		Generates and stores the generated coupons in the database
    		Each coupon is unique and generated once. Generation must fulfill following:-
    		1. store in database
    		2. must be 6 or 12 characters long (XXX-XXX)
    		4. each code must have indexing associated for data entry information about the distributor.
    		5. can include all keyboard type able (a-zA-Z0-9) characters
    		6. each must be unique

    		Each generated coupon must be stored in db.
    		Each will have used status.
    		Each coupon will have one to one relationship with:-
    			a. userid
    			b. examcode
    			c. distributor
    			d. status (used/free)    			
    	'''
        import random
        for i in range(0,90):
            number_system = 'zAyBxCwDvEuFt9GsH8rI7qJp6KoLnM5mNlOk4PjQih3RgSfTeU2dVcWbXa1YZz0'
            num  = random.randint(999999999, pow(62,6))
            coupon = ''
            while(num>62):
                rem = num%62
                num = num/62    
                coupon = coupon + number_system[rem]
            coupon = coupon + number_system[num]
            print self.db_object.get_one(self.table_name, {'code':str(coupon)})
            if self.db_object.get_one(self.table_name,{'code':str(coupon)}) is None:
                data = {
                    'code':coupon,
                    'subscription_type':subscription_type, 
                    'used':{'status':0}
                    }
                self.db_object.insert_one(self.table_name, data)
        return 'generated'            

  
    def validate_coupon(self, coupon_code):
    	'''Checks the validity of coupon'''
    	return self.db_object.get_one(self.table_name, {'code':coupon_code, 'used.status':0})

    def change_used_status_of_coupon(self, coupon_code, userid, examcode):
    	'''
    		For sample code for which one to many relationship exists. For rest
    		the one to one mapping exists.
    	'''
        request_time  = datetime.datetime.now()
        request_time  = time.mktime(request_time.timetuple())
        return self.db_object.update_upsert(self.table_name, {'code':coupon_code},{
                'used':{
                'status':1,
                'usedetails':{
                    'userid':int(userid), 
                    'examcode':str(examcode), 
                    'entrytime':request_time
                    }}})

    def check_subscried(self, exam_code,user_id):
        result = self.db_object.get_one(self.table_name, {'used.usedetails.examcode':str(exam_code), 'used.usedetails.userid':int(user_id)})
        print result
        if result == None:
            return False
        else:
            return True

# coupon = Coupon()        
# coupon.generate_coupons('Single Exam')