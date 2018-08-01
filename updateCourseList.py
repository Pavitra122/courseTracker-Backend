import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests





def returnDepartmentList():

	departments = []
	url = 'https://courses.illinois.edu/schedule/2018/fall'
	r = requests.get(url, timeout=5)
	soup = BeautifulSoup(r.content,'html.parser')
	datastring = soup.find_all('table')
	datastring =  datastring[0].tbody.find_all('td')

	for i, item in zip(range(len(datastring)), datastring):
		if i%2 == 0:
			departments.append(item.text.strip())

	return (departments)

def returnCoursesForDept(department):

	courses = []
	url = 'https://courses.illinois.edu/schedule/2018/fall/' + department
	r = requests.get(url, timeout=5)
	soup = BeautifulSoup(r.content,'html.parser')
	soup = soup.table.tbody.find_all('td')

	for i, item in zip(range(len(soup)), soup):
		if i%2 == 0:
			courses.append(item.text.strip().split()[1])


	return courses


def populateCourses():

	scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
	client = gspread.authorize(creds)
	print ("Initializing")
	sheet = client.open("Department and courses").sheet1

	#courses = {}
	departments =  returnDepartmentList()
	for index ,department in zip( range(len(departments)) ,departments):
		print (department)
		a = returnCoursesForDept(department)
		#courses[department] = a
		sheet.insert_row([department]+ [i for i in a] , index+1)

	#print courses



populateCourses()
