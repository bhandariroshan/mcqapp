from MongoConnection import MongoConnection
import time
import datetime
from bson import ObjectId


class Referral():

    def __init__(self):
        self.db_object = MongoConnection("localhost", 27017, 'mcq')
        self.table_name = 'referral'
        self.db_object.create_table(self.table_name, '_id')

    def get_referral_id(self, user_id):
        ref_id = self.db_object.get_one(
            self.table_name, {'useruid': int(user_id)}
        )
        if ref_id is not None:
            return ref_id['uid']['id']
        else:
            self.db_object.insert_one(
                self.table_name,
                {'useruid': int(user_id), 'invite_accept_ids': []}
            )
            ref_id = self.db_object.get_one(
                self.table_name, {'useruid': int(user_id)}
            )
            return ref_id['uid']['id']

    def update_invite_accept_list(self, ref_id, user_id):
        accept_time = datetime.datetime.now()
        accept_time = time.mktime(accept_time.timetuple())
        self.db_object.update_upsert_push(
            self.table_name,
            {'_id': ObjectId(ref_id)},
            {'invite_accept_ids':
                {'useruid': int(user_id), 'accept_time': accept_time}}
        )
