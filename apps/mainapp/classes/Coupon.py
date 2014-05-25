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
        for i in range(0,40):
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

  
    def validate_coupon(self, coupon_code, exam_category=None, exam_family=None):
    	'''Checks the validity of coupon'''
        coupon = self.db_object.get_one(self.table_name, {'code':coupon_code, 'used.status':0})
        # print exam_family, coupon, coupon_code, exam_category
        if coupon != None and coupon['subscription_type']=='IDP':
            return True
        elif coupon != None and coupon['subscription_type'] == exam_category:
            return True
    	elif coupon!=None and (coupon['subscription_type'] == exam_family):
            return True
        else:
            return False


    def get_coupon_by_coupon_code(self, coupon_code):
        return self.db_object.get_one(self.table_name, {'code':coupon_code})

    def change_used_status_of_coupon(self, coupon_code, user_name):
    	'''
    		For sample code for which one to many relationship exists. 
    	'''
        request_time  = datetime.datetime.now()
        request_time  = time.mktime(request_time.timetuple())    
        return self.db_object.update_upsert(self.table_name, {'code':coupon_code},{'used':{'status':1}})


# 1. DPS (Daily Practice Set)
# 2. CPS (Competitive Pracice Set)
# 3. MBBS-IOM-071
# 4. BE-IOE-071
# 5. IDP (Inter Disciplinary Plan)

# coupon = Coupon()        
# coupon.generate_coupons('IDP')
# coupon.generate_coupons('DPS')
# coupon.generate_coupons('CPS')
# coupon.generate_coupons('BE-IOE-071')
# coupon.generate_coupons('MBBS-IOM-071')