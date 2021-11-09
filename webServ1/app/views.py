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
        date = checkDate()
        song = {
            "song": db.getSongOfDay(date)
        }
        return jsonify(song)

#Gets the song of the day as a youtube link and if there is no song then generates one for that day
class GetSongOfTheDayYTLink(Resource):
    def get(self):
        date = checkDate()
        song = {
            "link": db.getSongOfDay(date,'link')
        }
        return jsonify(song)

api.add_resource(GetSongOfTheDay,'/')
api.add_resource(GetSongOfTheDayYTLink,'/link')