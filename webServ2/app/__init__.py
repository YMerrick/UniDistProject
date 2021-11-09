from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')
from app import views

db = SQLAlchemy(app)
db.create_all()