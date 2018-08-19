
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request, jsonify
import tracker
#import updateSectionList
import sys, os, traceback
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading
from flask_cors import CORS
import json

application  = Flask(__name__)
CORS(application)

#sheet.update_cell(1, 1, "My name is pavitra")
#row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
#index = 2
#sheet.delete_row(index)
#sheet.insert_row(row, index)


trackedClasses= []
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
print ("Initializing Credentials")
client = gspread.authorize(creds)
print ("Credentials Initializing")
sheet = client.open("courses").sheet1

def updateLoop():

	flag = 0
	for j in range(10000):
		try:
				trackedClasses = sheet.get_all_records()
				print ('Updating')
				if flag ==0:
					time.sleep(300)
				for i in range(len(trackedClasses)):
					#trackedClasses[i]['status'] = tracker.returnClassStatus(trackedClasses[i]['department'],trackedClasses[i]['courseNumber'], trackedClasses[i]['CRN'])
					trackedClasses[i]['status'] = j
					sheet.update_cell(i+2,5,trackedClasses[i]['status'])
				flag = 0

		except Exception as e:
			print (e)
			print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			scope = ['https://spreadsheets.google.com/feeds',
			         'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Re Authorizing")
			sheet = client.open("courses").sheet1
			flag = 1




t1 = threading.Thread(target=updateLoop, args=())
t1.start()

'''
@application.route('/v1/get_departments',methods=['GET'])
def getDepartments():
		try:
			scope = ['https://spreadsheets.google.com/feeds',
			         'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			depSheet = client.open("Department and courses").sheet1
			list = depSheet.col_values(1)
			return jsonify(list[1:])
		except Exception as e:
			print (e)
			print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			scope = ['https://spreadsheets.google.com/feeds',
			         'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Re Authorizing")
			depSheet = client.open("Department and courses").sheet1
			return jsonify(e)


@application.route('/v1/get_course_numbers',methods=['POST'])
def get_course_numbers():

	if request.method == 'POST':
		args=json.loads(request.data)
		print args
		deparment = args["department"]
		try:
			scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			depSheet = client.open("Department and courses").sheet1
			list = depSheet.col_values(1)
			for i in range(len(list)):
				if list[i] == deparment:
					classes = depSheet.row_values(i+1)[1:]
					return jsonify(classes)

			return jsonify("Department not found")
		except Exception as e:
			print (e)
			print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Re Authorizing")
			depSheet = client.open("Department and courses").sheet1
			return jsonify(e)
'''

@application.route('/v1/get_course',methods=['POST'])
def get_course():

	if request.method == 'POST':
		args=json.loads(request.data)
		print (args)
		crn = args["crn"]
		#print "CRN",crn
		try:
			scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			depSheet = client.open("Department and courses").get_worksheet(2)

			list = depSheet.col_values(1)
			for i in range(len(list)):
				#print (list[i])
				if list[i] == crn:
					course = depSheet.row_values(i+1)[1:]
					return jsonify(course)

			return jsonify({'success' : 0 ,'message' : 'CRN not found'})
		except Exception as e:
			print (e)
			print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('Project-f939c591cfa1.json', scope)
			client = gspread.authorize(creds)
			print ("Re Authorizing")
			depSheet = client.open("Department and courses").sheet1
			return jsonify({'success': 0 , 'message' :e})


@application.route('/')
def hello_world():
    return '<h1>Course Tracker</h1><p>A prototype API</p>'



@application.route('/v1/updateSectionList')
def updateDatabases():
	try:
		print ("Started updating database")
		#updateSectionList.updateSections()
		return "Success"
	except:
		return "Failure"


@application.route('/v1/', methods=['GET'])
def resources():
    return jsonify(['resources'])




#http://localhost:5000/v1/course_track/add?department=ECE&courseNumber=120&CRN=65253
#http://localhost:5000/v1/course_track/add?department=ECE&courseNumber=120&CRN=64598

@application.route('/v1/course_track/add', methods=['POST'])
def add():
	try:
		trackedClasses = sheet.get_all_records()
		print (request.data)
        #print (json.loads(request.content.decode('utf-8')))
		args = json.loads(request.data)
		courseNumber = int(args['courseNumber'])
		department = args['department']
		CRN = int(args['CRN'])
		# if 'courseNumber' in request.args:
		#     courseNumber = int(request.args['courseNumber'])
		# if 'department' in request.args:
		#     department = request.args['department']
		# if 'CRN' in request.args:
		#     CRN = int(request.args['CRN'])

		for i in range(len(trackedClasses)):
			if int(trackedClasses[i]['CRN']) == int(CRN):
				trackedClasses[i]['users'] = trackedClasses[i]['users'] + 1
				#sheet.delete_row(i+2)
				sheet.update_cell(i+2,4,trackedClasses[i]['users'] )
				#sheet.insert_row([ trackedClasses[i]['department'], trackedClasses[i]['courseNumber'],trackedClasses[i]['CRN'],trackedClasses[i]['users'],trackedClasses[i]['status'] ], i+2)
				return jsonify({ 'success' : 1 , 'message' : 'Increased number of users, new number = ' + str(trackedClasses[i]['users'])})


		if tracker.returnClassStatus(department,courseNumber,CRN) != 'Course Not found' :
			trackedClasses.append({'department':department, 'courseNumber':courseNumber, 'CRN':CRN  , 'users':1, 'status':tracker.returnClassStatus(department,courseNumber,CRN)})
			sheet.append_row([department, courseNumber, CRN  , 1, tracker.returnClassStatus(department,courseNumber,CRN)])
			return jsonify({'success' : 1 , 'message' : 'Added new course'})
		else:
			return jsonify({'success' : 0 ,'message' : 'Course Not found'})

	except Exception as e:
		print (e)
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
		return jsonify({'success' : 0 ,'message' :e})








#http://localhost:5000/v1/course_track/delete?department=ECE&courseNumber=120&CRN=65253
#http://localhost:5000/v1/course_track/delete?department=ECE&courseNumber=120&CRN=64598

@application.route('/v1/course_track/delete', methods=['GET'])
def remove():
	try:
		trackedClasses = sheet.get_all_records()
		if 'courseNumber' in request.args:
			courseNumber = int(request.args['courseNumber'])
		if 'department' in request.args:
			department = request.args['department']
		if 'CRN' in request.args:
			CRN = int(request.args['CRN'])

		for i in range(len(trackedClasses)):
			if int(trackedClasses[i]['CRN']) == int(CRN):
				trackedClasses[i]['users'] = trackedClasses[i]['users'] - 1
				if trackedClasses[i]['users'] == 0:
					del trackedClasses[i]
					sheet.delete_row(i+2)
					return jsonify({ 'message' : 'Not tracking class anymore'})
				sheet.update_cell(i+2,4,trackedClasses[i]['users'] )
				return jsonify({'message' :  'Decreased number of users, new number = ' +  str(trackedClasses[i]['users'])})
		return jsonify({'message': 'Some error occured'})

	except Exception as e :
		print(e)
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)










@application.route('/v1/course_track/returnClassStatus', methods=['GET'])
def status():
	try:
		if 'courseNumber' in request.args:
			courseNumber = int(request.args['courseNumber'])
		if 'department' in request.args:
			department = request.args['department']
		if 'CRN' in request.args:
			CRN = int(request.args['CRN'])
		print (department,courseNumber,CRN)
		return tracker.returnClassStatus(department,courseNumber,CRN)
	except Exception as e :
		print(e)
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)






@application.route('/v1/course_track/return_list', methods = ['GET'])
def returnArray():
    try:
        return jsonify(trackedClasses)
    except Exception as e :
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


if __name__ == "__main__":




    trackedClasses = sheet.get_all_records()



    application.run()
    t1.join()




'''
app.run()
while 1:
    print 'Hello'
    time.sleep(5)
    for i in range(len(trackedClasses)):
        trackedClasses[i]['status'] = tracker.returnClassStatus(trackedClasses[i]['department'],trackedClasses[i]['courseNumber'], trackedClasses[i]['CRN'])
        sheet.update_cell(i+2,5,trackedClasses[i]['status'])

'''

















#abcd
