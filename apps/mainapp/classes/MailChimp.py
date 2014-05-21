import mailchimp
from pymongo import Connection
from MongoConnection import MongoConnection


class MailChimp():
    """This class is used to make api calls to the MailChimp"""
    def __init__(self, list_id = 'f0b6e041eb'):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'mailchimp'
        self.list_id =  list_id
        self.db_object.create_table(self.table_name,'_id')
    
    def get_mailchimp_api(self):
        return mailchimp.Mailchimp('e9294366710f56f159569b82660f9df3-us3') #your api key here

    def save_mailchimp_response(self, doc):
        self.db_object.update_upsert(self.table_name, doc['data_sent'], doc)

    def subscribe(self, doc):
        try:
            first, last = doc['first_name'], doc['last_name']
            m = self.get_mailchimp_api()
            response = m.lists.subscribe(self.list_id, email = {'email':str(doc['email'])},
                double_optin = False,
                merge_vars = {"FNAME":str(first),"LNAME":str(last),
                'Name':str(doc['name'])},
                update_existing=True, send_welcome=True, replace_interests=True)
            self.save_mailchimp_response({'data_sent':doc, 'response':response})
            return {'status':1}
        except mailchimp.ListAlreadySubscribedError:
             return {'status':0,'message':'Already subscribed'}


