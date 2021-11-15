from app import db
from flask_sqlalchemy import SQLAlchemy

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songs = db.relationship('Song', backref='artist', lazy='dynamic', primaryjoin = (Song.artist_id == id))
    name = db.Column(db.String(200), index=True)

#code to create and populate database
"""db.create_all()

a = Artist(name = "Rick Astley")
db.session.add(a)
db.session.commit()

b = Artist.query.get(1)
s = Song(title = "Never Gonna Give You Up", artist_id = b.id)
db.session.add(s)

a = Artist(name = "Queen")
db.session.add(a)
db.session.commit()

b = Artist.query.get(2)
s = Song(title = "I Want To Break Free", artist_id = b.id)
db.session.add(s)

a = Artist(name = "Beatles")
db.session.add(a)
db.session.commit()

b = Artist.query.get(3)
s = Song(title = "Hey Jude", artist_id = b.id)
db.session.add(s)

db.session.commit()"""