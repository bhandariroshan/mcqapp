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

    def send_coupon_requested_email(self, request, name, phone, email):
        subject = 'New premium coupon request in MeroAnswer. '
        message_body = ''
        message_body = '\
        <table cellpadding="2" cellspacing="0">\
            <tr style="background-color:#6C7F40;">\
                <td style="width:30%; color: #fff;">Name</td>\
                <td style="width:50%; color: #fff;">Email</td>\
                <td style="width:20%; color: #fff;">Phone</td>\
            </tr>'
        
        message_body = message_body + '<tr>'
        message_body = message_body + '<td style="width:30%; font-size: 11px; color: #444;">' + str(name) + '\
        </td><td style="width:50%; font-size: 11px; color: #444;">' + str(email) + '</td>'
        message_body = message_body + '<td style="width:20%; font-size: 11px; color: #444;">'+ str(phone) + '</a></td>'
        message_body = message_body + '</tr>'

        message_body = message_body + '</table>'
        if request.user.is_authenticated():
            details = {'name':name, 'phone':phone, 'email':email, 'username':request.user.username}
        else:
            details = {'name':name, 'phone':phone, 'email':email}
        self.send_mail(
            subject, 
            [
                {'name':'main', 'content':message_body},
                {'name':'inbox','content':''''''}
            ], 
            [{'email':'brishi98@gmail.com'}, {'email':'info@phunka.com'}], details)