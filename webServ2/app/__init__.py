from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)
app.config.from_pyfile('config.py')
from app import views