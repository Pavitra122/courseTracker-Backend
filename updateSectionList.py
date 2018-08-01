import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
import json
import sys
import time




def getSections(row):

	deptName = row[0]
	courseNumbers = row[1:]

	returnList = []
	for number in courseNumbers:
		#time.sleep(5)
		sections = []
		print (number)
		url = "https://courses.illinois.edu/schedule/2018/fall/"
		url = url + str(deptName) + "/" + str(number)
		r = requests.get(url, timeout=25)
		soup = BeautifulSoup(r.content,'html.parser')

		datastring = soup.find_all('script')[3].text[26:-93]
		courses = json.loads(datastring)
		sections.append(str(deptName) + ' ' + str(number))
		for course in courses:

			soup =  BeautifulSoup(course['section'] ,'html.parser')
			#<div class="app-meeting">AD1</div>
			soup = soup.div.text
			print (soup)
			sections.append(soup)

		returnList.append(sections)

	return returnList



def updateSections():

	while 1:
		try:
			scope = ['https://spreadsheets.google.com/feeds',
			         'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Initializing")
			sheet2 = client.open("Department and courses").get_worksheet(1)
			sheet = client.open("Department and courses").sheet1

			departmentClasses = sheet.get_all_records()

			index = 279
			for deparment in departmentClasses[14:]:
				row = []
				row.append(deparment['department'])
				i = 1
				while deparment['course'+str(i)] != '':
					row.append(deparment['course'+str(i)])
					i = i+1
				print (row)
				rows = getSections(row)
				for row in rows:
					time.sleep(0.023529)  #Limiting to 90 requests per second
					if sheet2.cell(index,1).value == '':
						print ('writing row')
						time.sleep(0.5)
						sheet2.insert_row(row, index)
					else:
						print ('Not writing row')
					index = index +1
		except Exception as e:
			print (e)
			print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Re Authorizing - section update")



updateSections()




















#s
