from MongoConnection import MongoConnection
import mandrill 
        
class Email():
    def __init__ (self):        
        self.db_object = MongoConnection("localhost",27017,'mcq')
        self.table_name = 'emailbacklogs'
        self.db_object.create_table(self.table_name,'_id')

    def save_backlogs(self,doc):
        self.db_object.insert_one(self.table_name, doc)        

    def send_mail(self, subject, template_content=[{}], to = [{}]):
        md = mandrill.Mandrill('DS3yEW4HdOzqHGXOiXGPkg')
        # md = mandrill.Mandrill('NwotnhPk1Nprc6OX0Wq6vA')
        mes = mandrill.Messages(md)

        message = {
            'auto_html': False,
            'auto_text': False,
            'to':to,
            'from_email':'no-reply@meroanswer.com', 
            'from_name':'Meroanswer', 
            'important':'true',
            'track_click':'true',
            'subject':subject
        }
        
        template_content = template_content
        self.save_backlogs({'message':message, 'template_content':template_content})
        mes.send_template('foodtrade-master', template_content, message)