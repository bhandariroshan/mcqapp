from MongoConnection import MongoConnection
import datetime


class CouponCount():

    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'couponcount'
        self.db_object.create_table(self.table_name, '_id')

    def get_coupon_count(self):
        return self.db_object.get_one(self.table_name, {})

    def update_coupon_count(self, count):
        now = datetime.datetime.now()
        data = {
            'count': count,
            'timestamp': int(now.strftime("%s"))
        }
        return self.db_object.update_upsert(self.table_name, {}, data)

# a = CouponCount()
# print a.update_coupon_count(1200)
