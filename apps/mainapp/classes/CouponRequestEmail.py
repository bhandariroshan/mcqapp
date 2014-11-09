from MongoConnection import MongoConnection
import mandrill 
        
class CouponEmail():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'couponrequestlogs'
        self.db_object.create_table(self.table_name, '_id')

    def save_backlogs(self,doc):
        self.db_object.insert_one(self.table_name, doc)        

    def send_mail(self, subject, template_content=[{}], to = [{}], details ={}):
        md = mandrill.Mandrill('DS3yEW4HdOzqHGXOiXGPkg')
        mes = mandrill.Messages(md)

        message = {
            'auto_html': False,
            'auto_text': False,
            'to':to,
            'from_email':'no-reply@meroanswer.com', 
            'from_name':'MeroAnswer', 
            'important':'true',
            'track_click':'true',
            'subject':subject
        }
        
        template_content = template_content
        self.save_backlogs({'message':message, 'template_content':template_content, 'details':details})
        mes.send_template('foodtrade-master', template_content, message)