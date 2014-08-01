from django import template
from apps.mainapp.classes.email import Email
register = template.Library()


@register.filter
def error(value, args):
    email = Email()
    to = 'santosh.ghimire33@gmail.com'  # , 'brishi98@gmail.com']
    subject = args + ' Error in Meroanswer'
    msg = 'Meroanswer just encountered a ' + args + ' ' + 'error at ' + \
        value + '. Please fix this as soon as you can.'
    # print to, subject, msg
    # for each_receipent in to:
        # pass
    # email.send_mail(to=to, subject=subject, text=msg)
    return ''
