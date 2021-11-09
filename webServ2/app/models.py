from app import app
from flask_sqlalchemy import SQLAlchemy



class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    songs = db.Relationship('Song', backref = 'Song', lazy = 'dynamic')

