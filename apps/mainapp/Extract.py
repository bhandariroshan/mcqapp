#!/usr/bin/env python
# encoding: utf-8

from BeautifulSoup import BeautifulSoup
import HTMLParser

	
def get_content_table(full_html):
	sp = BeautifulSoup(full_html)
	matches = sp.findAll('table', attrs={"width":"100%", "border":"0", "cellpadding":"4", "class":"content"})
	for match in matches:
		return str(match)
	return ""


def get_subject_mark(row):
	sp = BeautifulSoup(str(row))
	tds = sp.findAll('td', attrs={"align":"left" ,"valign":"top", "bgcolor":"#D4DCE7"})
	if len(tds)<4:
		return { "status":"error"}
	marks_dic = {}
	h = HTMLParser.HTMLParser()
	marks_dic['subject'] = h.unescape(tds[0].text).encode('utf-8').strip()
	theory = tds[3].text
	
	marks_dic['theory_attempt'] = theory.count("#")
	theory = theory.replace("#","")
	marks_dic['theory'] =  h.unescape(theory).encode('utf-8').strip().replace('\xc2','').replace('\xa0','')

	practical = tds[4].text.encode('utf-8').strip()
	marks_dic['practical_attempt'] = practical.count("#")
	practical = practical.replace("#","")
	marks_dic['practical'] = h.unescape(practical).encode('utf-8').strip().replace('\xc2','').replace('\xa0','')

	total = tds[5].text.encode('utf-8').strip()
	marks_dic['total_obtained'] = h.unescape(total).encode('utf-8').strip().replace('\xc2','').replace('\xa0','')

	grace = tds[6].text.encode('utf-8').strip()
	marks_dic['grace_marks'] = h.unescape(grace).encode('utf-8').strip().replace('\xc2','').replace('\xa0','')



	
	return { "status":"ok","result":marks_dic}



def extract(page):
	if "Sorry...! You have failed!! Better luck next time." in page:	
		ret = {}
		ret['status']	= "last"
		ret['message'] = "Overflown"
		return ret
	if "You have an error in your SQL syntax;" in page:	
		ret = {}
		ret['status']	= "sqlerror"
		ret['message'] = "Sql error"
		return ret
	error = {"status":"error"}
	content = get_content_table(page)
	if content == "":
		ret = {}
		ret['status']	= "unknown"
		ret['message'] = "Unknown Error"
		return ret

	

	soup = BeautifulSoup(content)


	matches = soup.findAll('td', attrs={'colspan':'7','class': 'results'})


	## scraping name and sex
	try:
		name_sex = matches[0].text.split('(')
		name = name_sex[0].strip()
		sex = name_sex[1].replace(")","").strip()
	except:
		error['message'] = "Student Name or sex could not be extracted"
		return error

	## scraping 
	try:
		symbol_no = matches[2].text
	except:
		error['message'] = "Could not found symbol no"
		return error
	try:
		school_address = matches[3].text.replace("\r","").split(',\n')
		district = school_address[1].strip()
		school_street = school_address[0].split(" ")
		street = school_street[-1]
		school = " ".join(school_street[:-1])
	except:
		error['message'] = "Could not extract school and address"
		return error


	rows = soup.findAll('tr', attrs={})
	marks_list = []

	for row in rows:
		result = get_subject_mark(row)
		if result.get('status') == "ok":
			marks_list.append(result.get('result'))

	# print name+","+sex
	# print symbol_no
	# print district, street, school

	student_details = {"name":name, "sex":sex,"symbol":symbol_no,"district":district, "street":street, "school":school}
	if len(marks_list)>0:
		student_details['scores'] = marks_list
		return {"status":"ok", "result":student_details}
	else:
		error['message'] = "No marks"
		return error
