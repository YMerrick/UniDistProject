from flask import Flask, request, jsonify
from app import app

def testRun():
    global app
    app = Flask(__name__)

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