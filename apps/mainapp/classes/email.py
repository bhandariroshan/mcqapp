# from MongoConnection import MongoConnection
import mandrill


class Email():
    # def __init__ (self):
        # self.db_object = MongoConnection("localhost",27017,'mcq')
        # self.table_name = 'emailbacklogs'
        # self.db_object.create_table(self.table_name,'_id')

    def save_backlogs(self, doc):
        self.db_object.insert_one(self.table_name, doc)

    # def send_mail(self, subject, template_content=[{}], to = [{}]):
    def send_mail(self, subject, text, to):
        # md = mandrill.Mandrill('DS3yEW4HdOzqHGXOiXGPkg')  # roshan
        # md = mandrill.Mandrill('NwotnhPk1Nprc6OX0Wq6vA')  # foodtrade
        md = mandrill.Mandrill('IMFVH20W5FQYW5oO-DOHSQ')   # santosh@phunka

        message = {
            'auto_html': False,
            'auto_text': False,
            'to': [{
                'email': to,
                'name': 'Recipient Name',
                'type': 'to'
            }],
            'from_email': 'no-reply@meroanswer.com',
            'from_name': 'Meroanswer',
            'important': 'true',
            'track_click': 'true',
            'subject': subject,
            'text': text
        }

        result = md.messages.send(
            message=message, async=False, ip_pool='Main Pool'
        )
        # self.save_backlogs(
        #     {'message':message, 'template_content':template_content}
        # )
        # mes.send_template('meroanswer', template_content, message)

email = Email()
email.send_mail(
    'Test email', 'Just testing an email code',
    ['santosh.ghimire33@gmail.com']
)
