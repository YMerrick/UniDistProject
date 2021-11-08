from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from app import app
from .models import Model
from datetime import datetime

api = Api(app)
db = Model(app)

def testRun():
    global app
    app = Flask(__name__)

if __name__ == '__main__':
    testRun()    

print(__name__)

message = [{'message': ' Hello World '}]

'''@app.route("/")
def hello_world():
    return jsonify(message)

@app.route("/", methods= ['POST'])
def add_message():
    message.append(request.get_json())
    return '',204
'''
#Gets the date of today
def checkDate():
    today = datetime.now()
    todayDay = today.strftime('%d')
    todayMonth = today.strftime('%m')
    todayYear = today.strftime('%Y')
    date = todayDay + '-' + todayMonth + '-' + todayYear
    return date

#Gets the song of the day and if there is no song then generates one for that day
class GetSongOfTheDay(Resource):
    def get(self):
        return 0

#Gets the song of the day as a youtube link and if there is no song then generates one for that day
class GetSongOfTheDayYTLink(Resource):
    def get(self):
        pass

class HelloWorld(Resource):
    def get(self):
        return jsonify(message)

class AddResource(Resource):
    def put(self,messageIn):
        messageINN = {'message':messageIn}
        message.append(messageINN)
        return jsonify(message)
    
    def post(self,messageIn):
        for mlist in message:
            mlist['message'] = messageIn
        return '', 204

checkDate()
#api.add_resource(HelloWorld,'/')
#api.add_resource(AddResource,'/<messageIn>')