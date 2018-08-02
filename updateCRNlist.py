import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
import json
import sys
import time



def getCRN(row):

	try:
		deptName = row[0]
		courseNumbers = row[1:]
		returnList = []
		for number in courseNumbers:
			#time.sleep(5)
			print (number)
			url = "https://courses.illinois.edu/schedule/2018/fall/"
			if deptName == 'MUS' and number == '90':
				print('MUS 090 Exception occured !!!!!!')
				url = url + str(deptName) + "/" + str('090')
			else:
				url = url + str(deptName) + "/" + str(number)
			r = requests.get(url, timeout=25)
			soup = BeautifulSoup(r.content,'html.parser')

			datastring = soup.find_all('script')[3].text[26:-93]
			try:
				courses = json.loads(datastring)

				#sections.append(str(deptName) + ' ' + str(number))
				for course in courses:

					#print (course['crn'])
					returnList.append([course['crn'] , deptName , number])


			except Exception as e:
				print (e)
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
				print ("Error occured in course" + str(deptName) + str(number))
				return []

		return returnList
	except Exception as e:
		print (e)
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


def updateCRN():

	department = 131
	index = 7436
	while 1:

		try:

			scope = ['https://spreadsheets.google.com/feeds',
			         'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Initializing")
			sheet3 = client.open("Department and courses").get_worksheet(2)
			sheet = client.open("Department and courses").sheet1
			departmentClasses = sheet.get_all_records()
			#time.sleep(10)
			index_temp = index
			department_temp = department
			for deparment in departmentClasses[department_temp:]:

				row = []
				row.append(deparment['department'])
				i = 1

				while deparment['course'+str(i)] != '' and i < sheet.col_count - 1:
					row.append(deparment['course'+str(i)])
					i = i+1

				print (row)
				rows = getCRN(row)
				for row in rows:
					time.sleep(2)  #Limiting to 98.333 requests per second

					print (index_temp)
					if sheet3.cell(index_temp,1).value == '':
						print ('writing row')
						#print row
						#time.sleep(1.5)
						sheet3.insert_row(row, index_temp)
						index_temp = index_temp +1
					else:
						print ('Not writing row')
						index_temp = index_temp +1
				department = department + 1
				index = index_temp
		except Exception as e:
			print (e)
			print ("Sleeping for 100 seconds")
			time.sleep(100)
			print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Re Authorizing - section update")



updateCRN()
