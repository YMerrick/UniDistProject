from app import db
from flask_sqlalchemy import SQLAlchemy

#database models
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    #define the relation to the artist model
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #define the one to many relation between artist and song
    songs = db.relationship('Song', backref='artist', lazy='dynamic', primaryjoin = (Song.artist_id == id))
    name = db.Column(db.String(200), index=True)

#Remove all information from the string that is not the song name e.g. featuring artists
def superStrip(songName):
    songName = songName.split('(Official',1)[0]
    songName = songName.split('(official',1)[0]
    songName = songName.split('(Visualizer',1)[0]
    songName = songName.split('(Visualiser',1)[0]
    songName = songName.split('[Official',1)[0]
    songName = songName.split('[OFFICIAL',1)[0]
    songName = songName.split('(Lyric')[0]
    songName = songName.split('(lyric')[0]
    songName = songName.split('(PNAU',1)[0]
    songName = songName.split('(Remix',1)[0]
    songName = songName.split('Remix')[0]
    songName = songName.split('Acoustic',1)[0]
    songName = songName.split('ft.',1)[0]
    songName = songName.split('Ft.',1)[0]
    songName = songName.split('(feat',1)[0]
    songName = songName.split('feat.',1)[0]
    songName = songName.split('Featuring',1)[0]
    songName = songName.split('(First',1)[0]
    songName = songName.split('(clip',1)[0]
    songName = songName.split('(Feat',1)[0]
    songName = songName.split('(Video',1)[0]
    songName = songName.split('Official',1)[0]
    songName = songName.split('(with',1)[0]
    songName = songName.split('[Music',1)[0]
    songName = songName.split('(OFFICIAL',1)[0]
    return songName

#Takes a line from a file stips all unnecessary information and returns a tuple
def stripper(line):
    #strips and stores the yt code
    noYTLine = line.rsplit(' ',1)
    ytCode = noYTLine[1].strip()
    noYTLine[0] = noYTLine[0].replace('Anne-Marie','AnneMarie')
    noYTLine[0] = noYTLine[0].replace('Angel-A','AngelA')
    noYTLine[0] = noYTLine[0].replace('K-391','K391')
    noYTLine[0] = noYTLine[0].replace(b'\xe2\x80\x94'.decode('utf-8'),'-')
    
    #If the song does not contain a - to serparate song writer and name
    if noYTLine[0].find('-') == -1:
        songName = superStrip(noYTLine[0])
        songName = songName.strip()
        return (songName,ytCode)
    #If the song does contain a - to serparate the song writer and name
    else:
        artistName = noYTLine[0].split(' -',1)[0]
        artistName = artistName.split(',',1)[0]
        artistName = artistName.split('&',1)[0]
        noYTLine = noYTLine[0].split('-',1)[1]
        songName = superStrip(noYTLine)
        songName = songName.strip()
        return (artistName,songName,ytCode)

#Code used to create database and populate database using a file of songs and artists
"""
db.create_all()

#a couple of manual enteries

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
s = Song(title = "Bohemian Rhapsody", artist_id = b.id)
db.session.add(s)

#open the file, parse the file and store the parsed information in the database 

with open('/home/csunix/sc19ti/comp3211/Coursework_2/comp3211/webServ2/app/My YouTube Playlist.txt', 'r',encoding = 'utf-8') as f:
        i = 3
        for line in f:
            data = stripper(line)
            
            a = Artist(name = data[0])
            db.session.add(a)
            db.session.commit()

            b = Artist.query.get(i)
            s = Song(title = data[1], artist_id = b.id)
            db.session.add(s)
            db.session.commit()
            i += 1
"""
