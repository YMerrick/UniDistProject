from flask import Flask, request, jsonify
from app import app, models
from flask_restful import Resource, Api


def testRun():
    global app
    app = Flask(__name__)

#inialise the RESTful API    
api = Api(app)

if __name__ == '__main__':
    testRun()    

print(__name__)

class GetArtist(Resource):
    def get(self, song):
        #replace underscores with whitespace
        song = song.replace("_", " ")
        #query the Song table for this input
        song_record = models.Song.query.filter_by(title=song).all()
        #error handling if the song cannot be found
        if not song_record:
            return "Song not found"
        #query the database for the artist for this particular song
        artist = models.Artist.query.get(song_record[0].artist_id)
        if not artist:
            return "Artist not found"        
        return artist.name

#add the GetArtist resource to the RESTful API
api.add_resource(GetArtist, '/song/<string:song>', methods = ['GET'])