from apps.mainapp.classes.MongoConnection import MongoConnection
import time, datetime

class Coupon():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcqapp')
        self.table_name = 'coupons'
        self.db_object.create_table(self.table_name,'_id')

    def generate_coupons(self):
    	'''
    		Generates and stores the generated coupons in the database
    		Each coupon is unique and generated once. Generation must fulfill following:-
    		1. 2 or more secret password for generation (so that validity can be checked later)
    		2. must be 8 or 12 characters long (XXX-XXX-XXX-XXX)
    		3. generation time must be infinite under brute force approach
    		4. each code must have indexing associated for data entry information about the distributor.
    		5. can include all keyboard type able (a-zA-Z0-9!~#$%^&*) characters
    		6. each must be unique

    		Each generated coupon must be stored in db.
    		Each will have used status.
    		Each coupon will have one to one relationship with:-
    			a. userid
    			b. examcode
    			c. distributor
    			d. status (used/free)
    			e. 
    	'''
    	pass

    def validate_coupon(self, coupon_code):
    	'''Checks the validity of coupon'''
    	return self.db_object.get_one(self.table_name, {'code':coupon_code, 'used.status':0})

    def change_used_status_of_coupon(self, coupon_code, userid, examcode):
    	'''
    		For sample code for which one to many relationship exists. For rest
    		the one to one mapping exists.
    	'''
        return self.db_object.update_upsert(self.table_name, {
            'code':coupon_code},{
                'used':{
                'status':1,'usedetails':{
                    'userid':userid, 'examcode':examcode, 'entrytime':int(datetime.datetime.now())
                    }}})