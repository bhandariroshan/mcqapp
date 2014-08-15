from MongoConnection import MongoConnection
import time
import datetime


class Coupon():

    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'coupons'
        self.db_object.create_table(self.table_name, '_id')

    def generate_coupons(self, subscription_type):
        '''
            Generates and stores the generated coupons in the database
            Each coupon is unique and generated once.
            Generation must fulfill following:-
            1. store in database
            2. must be 6 or 12 characters long (XXX-XXX)
            4. each code must have indexing associated for data entry
                information about the distributor.
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
        count = 0
        while count < 200:
            number_system = 'zAyBxCwDvEuFt9GsH8r7qJp6KoLnM5mNOk4PjQih3Rg\
            SfTeU2dVcWbXa1YZz0'
            num = random.randint(999999999, pow(60, 6))
            coupon = ''
            while(num > 60):
                rem = num % 60
                num = num / 60
                coupon = coupon + number_system[rem]
            coupon = coupon + number_system[num]
            if coupon.find(' ') != -1:
                coupon = coupon.replace(' ', '')
            if len(coupon) < 6:
                continue

            if self.db_object.get_one(
                self.table_name, {'code': str(coupon)}
            ) is None:
                request_time = datetime.datetime.now()
                gen_time = time.mktime(request_time.timetuple())
                data = {
                    'code': coupon,
                    'subscription_type': subscription_type,
                    'used': {'status': 0},
                    'printed': False,
                    'generated_time': gen_time
                }
                self.db_object.insert_one(self.table_name, data)
            count += 1
        return 'generated'

    def validate_coupon(self, coupon_code, exam_category=None,
                        exam_family=None):
        '''Checks the validity of coupon'''
        coupon = self.db_object.get_one(
            self.table_name, {'code': coupon_code, 'used.status': 0}
        )
        if coupon is not None and coupon['subscription_type'] == 'IDP':
            return True
        elif coupon is not None and coupon['subscription_type'] == \
                exam_category:
            return True
        elif coupon is not None and (
            coupon['subscription_type'] == exam_family
        ):
            return True
        else:
            return False

    def has_susbcription_plan_in_coupon(self, coupon_code):
        coupon = self.db_object.get_one(
            self.table_name, {'code': coupon_code, 'used.status': 0}
        )
        if coupon is not None and coupon['subscription_type'] == 'IDP':
            return True
        elif coupon is not None and (
            coupon['subscription_type'] == 'BE-IOE' or
            coupon['subscription_type'] == 'MBBS-IOM'
        ):
            return True
        else:
            return False

    def get_coupon_by_coupon_code(self, coupon_code):
        return self.db_object.get_one(
            self.table_name,
            {'code': coupon_code}
        )

    def get_unused_coupon_by_coupon_code(self, coupon_code):
        return self.db_object.get_one(
            self.table_name,
            {'code': coupon_code,
             'used.status': 0}
        )

    def change_used_status_of_coupon(self, coupon_code, user_name):
        '''
            For sample code for which one to many relationship exists.
        '''
        request_time = datetime.datetime.now()
        request_time = time.mktime(request_time.timetuple())
        return self.db_object.update_upsert(
            self.table_name,
            {'code': coupon_code},
            {'used': {'status': 1, 'used_time': request_time}}
        )

    def get_coupons(self, subscription_type):
        return self.db_object.get_all_vals(
            self.table_name,
            {'subscription_type': subscription_type,
             'used.status': 0,
             'printed': False}
        )

    def update_coupons(self, subscription_type):
        return self.db_object.update_multi(
            self.table_name,
            {'subscription_type': subscription_type},
            {'printed': True}
        )

    def update_serial_no(self, serial_no, coupon_code):
        return self.db_object.update(
            self.table_name,
            {'code': coupon_code},
            {'serial_no': serial_no,
             'printed': True}
        )

    def search_by_code_or_serial(self, query, int_code=None):
        if int_code is None:
            return self.db_object.get_one(self.table_name, {'code': str(query)})
        else:
            return self.db_object.get_one(self.table_name, {'serial_no': int_code})
