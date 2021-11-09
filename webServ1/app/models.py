from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from random import choice
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
    
    def getSongFromDate(self,tDate):
        self.dateCheck(tDate)
        session = self.db.session
        dbQuery = (
            session.query(self.SongTable.songName)
            .select_from(self.DateTable)
            .filter_by(date = tDate)
            .join(self.SongTable, self.SongTable.songKey == self.SongDateTable.songKey)
            .join(self.SongDateTable, self.SongDateTable.dateKey == self.DateTable.dateKey)
            .first()
        )
        if dbQuery != None:
            return dbQuery[0]
        else:
            return dbQuery

    def getDateKey(self,tDate):
        session = self.db.session
        dbQuery = (
            session.query(self.DateTable.dateKey)
            .filter_by(date = tDate)
            .first()
        )
        if dbQuery == None:
            self.addDate(tDate)
            return self.getDateKey(tDate)
        else:
            session.close()
            return dbQuery[0]

    def addDate(self,tDate):
        session = self.db.session
        newDate = self.DateTable(date = tDate)
        session.add(newDate)
        session.commit()
        session.close()
        
    def songCheck(self,songID):
        session = self.db.session
        dbQuery = (
            session.query(self.SongDateTable.songKey)
            .filter_by(songKey = songID)
            .first()
        )
        if dbQuery != None:
            return True
        else:
            return False

    #program checks if the date exists and if it doesn't then inputs it into the db
    def dateCheck(self,tDate):
        session = self.db.session
        dbQuery = (
            session.query(self.DateTable)
            .filter_by(date = tDate)
            .count()
        )
        if dbQuery == 0:
            self.addDate(tDate)

    def getSongList(self):
        session = self.db.session
        dbQuery = session.query(self.SongTable.songKey).all()
        session.close()
        return dbQuery

    def getSongByKey(self,key):
        session = self.db.session
        dbQuery = session.query(self.SongTable.songName).filter_by(songKey = key).first()
        if dbQuery != None:
            return dbQuery[0]
        return dbQuery
    
    def getSongLinkByKey(self,key):
        session = self.db.session
        dbQuery = session.query(self.SongTable.ytLink).filter_by(songKey = key).first()
        if dbQuery != None:
            return 'https://www.youtube.com/watch?v='+dbQuery[0]
        return dbQuery


    def getSongLinkFromDate(self, tDate):
        self.dateCheck(tDate)
        session = self.db.session
        dbQuery = (
            session.query(self.SongTable.ytLink)
            .select_from(self.DateTable)
            .filter_by(date = tDate)
            .join(self.SongTable, self.SongTable.songKey == self.SongDateTable.songKey)
            .join(self.SongDateTable, self.SongDateTable.dateKey == self.DateTable.dateKey)
        ).first()
        if dbQuery == None:
            return None
        return  'https://www.youtube.com/watch?v='+dbQuery[0]

    #Generates a song of the day
    #Checks to see if there is an entry and if not then generates a new one
    #if there is an entry then it returns the one stated
    def getSongOfDay(self, tDate,type = 'name'):
        self.dateCheck(tDate)
        songOD = self.getSongFromDate(tDate)
        

        #if there is no song then it generates a random number and picks the song
        if songOD == None:
            listOSongs = self.getSongList()
            songID = choice(listOSongs)[0]
            while self.songCheck(songID):
                songID = choice(listOSongs)[0]
            newSD = self.SongDateTable(songKey = songID,dateKey = self.getDateKey(tDate))
            session = self.db.session
            session.add(newSD)
            session.commit()
            session.close()
            if type == 'name':
                return self.getSongByKey(songID)
            elif type == 'link':
                return self.getSongLinkByKey(songID)
            else:
                return None
            #After song has been picked the program then inputs into the db and returns song name
        else:
            if type == 'name':
                return songOD
            elif type == 'link':
                return self.getSongLinkFromDate(tDate)
            else:
                return None