#!/usr/bin/env python
# encoding: utf-8
import HTMLParser
from bs4 import BeautifulSoup
import requests


def get_html_ntc(symbol_no, date_of_birth):
    # try:
    request_url = 'http://slc.ntc.net.np/slc2070_ledger.php'
    payload = {
    	'symbol':symbol_no,
    	'dob':date_of_birth,
        'submit':'Submit'
    }    
    r = requests.post(request_url, payload)
    soup = BeautifulSoup(r.text)
    matches = soup.findAll('td', {'valign':'top'})
    html_parser = HTMLParser.HTMLParser()
    
    subjects = html_parser.unescape(str(matches[0])).replace('<td valign="top">','').replace('</td>','').split('<br><br>')[0:8]

    new_subjects = []
    for eachSubject in subjects:
        eachSubject = eachSubject.replace("\n",'').replace('\t','').replace('<br>','').replace('<br/>','').replace('</br>','')
        new_subjects.append(eachSubject)

    
    theory = html_parser.unescape(str(matches[1])).replace('<td valign="top"><div align="center">','').replace('</div></td>','').split('<br><br>')[0:8]
    theory_marks = []
    for eachSubject in theory:
        eachSubject = eachSubject.replace("\n",'').replace('\t','').replace('<br>','').replace('<br/>','').replace('</br>','')
        theory_marks.append(eachSubject)

    practical = html_parser.unescape(str(matches[2])).replace('<td valign="top"><div align="center">','').replace('</div></td>','').split('<br><br>')[0:8]
    practical_marks = []
    for eachSubject in practical:
        eachSubject = eachSubject.replace("\n",'').replace('\t','').replace('<br>','').replace('<br/>','').replace('</br>','')
        practical_marks.append(eachSubject)

    
    total = html_parser.unescape(str(matches[3])).replace('<td valign="top"> <div align="right">','').replace('</div></td>','').split('<br><br>')[0:8]
    total_marks = []
    for eachSubject in total:
        eachSubject = eachSubject.replace("\n",'').replace('\t','').replace('<br>','').replace('<br/>','').replace('</br>','')
        total_marks.append(eachSubject)
    

    return_list = []
    # return {'subjects':len(new_subjects), 'practical':len(practical_marks), 'theory':len(theory_marks), 'total':len(total_marks)}
    for i in range(0,len(new_subjects)):
        marks_dic = {}
        marks_dic['subject'] = new_subjects[i]        
        marks_dic['theory'] =  theory_marks[i]
        marks_dic['practical'] = practical_marks[i]
        marks_dic['total_obtained'] = total_marks[i]
        return_list.append(marks_dic)
    
    student_details = {"name":"", "sex":"","symbol":symbol_no,"district":"", "street":"", "school":"", "status":"ok", 'scores':return_list}
    return_val = {'status':'ok', 'result':student_details}
    return return_val
    # except:
    #     return {'status':"error", 'message':'no result'}

print get_html_ntc(symbol_no='0295639', date_of_birth='2054-09-20')