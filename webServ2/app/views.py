from flask import Flask, request, jsonify
from app import app, models
from flask_restful import Resource, Api
#import requests

def testRun():
    global app
    app = Flask(__name__)
    
api = Api(app)

if __name__ == '__main__':
    testRun()    

print(__name__)

class GetArtist(Resource):
    
    def get(self, song):
        song = song.replace("_", " ")
        song_record = models.Song.query.filter_by(title=song).all()
        artist = models.Artist.query.get(song_record[0].artist_id)
        if not artist:
            return "Song not found"
        
        #This will send the request to the external service, commented out for now while the external client has not been implemented
        #external_client = requests.post("*url of external service*" + artist.name)
        #for now, just return result to the user
        return artist.name

api.add_resource(GetArtist, '/song/<string:song>', methods = ['GET'])