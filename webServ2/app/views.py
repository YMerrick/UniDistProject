from flask import Flask, request, jsonify
from app import app
from flask_restful import Resource, Api

def testRun():
    global app
    app = Flask(__name__)
    
api = Api(app)

if __name__ == '__main__':
    testRun()    

print(__name__)

message = [{'message': ' Hello World '}]

@app.route("/")
def hello_world():
    return jsonify(message)

@app.route("/", methods= ['POST'])
def add_message():
    message.append(request.get_json())
    return '',204

class GetArtist(Resource):
    def get(self):
        return {'hello':'world'}

api.add_resource(GetArtist, '/hello')