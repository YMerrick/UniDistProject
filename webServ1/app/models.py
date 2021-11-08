from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

class Model():

    def __init__(self, app):
        #Instantiating the db
        self.db = SQLAlchemy(app)
        base = automap_base()
        base.prepare(self.db.engine, reflect = True)

        #Variables to access the tables
        self.SongTable = base.classes.SongTable
        self.DateTable = base.classes.DateTable
        self.SongDateTable = base.classes.SongDateTable
    
    def getSongFromDate(self,tDate = None):
        pass

    def getSongLinkFromDate(self, tDate = None):
        pass

    #Generates a song of the day
    #Checks to see if there is an entry and if not then generates a new one
    #if there is an entry then it returns the one stated
    def genSongOfDay(self, tDate):
        pass