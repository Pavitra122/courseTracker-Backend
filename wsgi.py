from flask import Flask
application = Flask(__name__)

@application.route("/")
def hello():
    return "<h1>Course Tracker</h1><p>A prototype API</p>"

if __name__ == "__main__":
    application.run()
