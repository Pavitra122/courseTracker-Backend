# Generated the requirements.txt file by the pipreqs module from the internet.
# Just type $ pipreqs /home/project/location to genereate the file.
# https://github.com/bndr/pipreqs

from bs4 import BeautifulSoup
import requests
import sys
import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#from user_agent import generate_user_agent
#from playsound import playsound



def returnClassStatus(className, classNumber, CRN):

	try:
		url = "https://courses.illinois.edu/schedule/2018/fall/"
		url = url + str(className) + "/" + str(classNumber)

		r = requests.get(url, timeout=5)
		soup = BeautifulSoup(r.content,'html.parser')

		datastring = soup.find_all('script')[3].text[26:-93]
		courses = json.loads(datastring)


		for course in courses:
			if int(CRN) == int(course['crn']):
				if course['availability'] != 'Open' and course['availability'] != 'Open (Restricted)':
					return 'Closed'
				else:
					return 'Open'
		return 'Course Not found'
	except Exception as e :
		print(e)
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)





#s
