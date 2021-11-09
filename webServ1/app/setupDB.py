import sqlite3
import os

#Checks if songs.db exist and if it does then checks if it contains information

#Connect to the database
def createCon(dfile='songs.db'):
    thisDir = os.path.abspath(os.path.dirname(__file__))
    connection = sqlite3.connect(thisDir+'\\' + dfile)
    return connection

#Creates tables required
#passes a connection
def createTables(con):
    db = con.cursor()
    songTableQ = ''' CREATE TABLE IF NOT EXISTS SongTable (
                                                songKey integer PRIMARY KEY,
                                                songName text NOT NULL,
                                                ytLink text
                                                ); '''
    dateTableQ = ''' CREATE TABLE IF NOT EXISTS DateTable (
                                                dateKey integer PRIMARY KEY,
                                                date text NOT NULL
                                                ); '''
    sdTableQ = ''' CREATE TABLE IF NOT EXISTS   SongDateTable (
                                                songDatekey integer PRIMARY KEY,
                                                songKey integer NOT NULL,
                                                dateKey integer NOT NULL,
                                                FOREIGN KEY (songKey) REFERENCES SongTable(songKey),
                                                FOREIGN KEY (dateKey) REFERENCES DateTable(dateKey)
                                                ); '''

    db.execute(songTableQ)
    db.execute(dateTableQ)
    db.execute(sdTableQ)
    con.commit()
    

def cleanList(nlist):
    newList = []
    for item in nlist:
        newList.append(item[0])
    return newList

#Checks tables if they exist
#Passes a cursor
def checkTables(con):
    tableList = ['SongTable','DateTable','SongDateTable']
    db = con.cursor()
    query = '''SELECT name FROM sqlite_master WHERE type = 'table'; '''
    db.execute(query)
    dblist = cleanList(db.fetchall())
    flag = True
    for item in dblist:
        if item in tableList:
            continue
        else:
            flag = False
    return flag

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
        noYTLine = noYTLine[0].split('-',1)[1]
        songName = superStrip(noYTLine)
        songName = songName.strip()
        return (songName,ytCode)


#Takes a text file and loads the contents into a list of tuples
def loadFile(fname):
    songList = list()
    with open(fname, 'r',encoding = 'utf-8') as f:
        for line in f:
            songList.append(stripper(line))
    return songList

#adds list of songs to the db
def addSongs(con):
    db = con.cursor()
    fname = 'My YouTube Playlist.txt'
    songList = loadFile(fname)
    for item in songList:
        insertQ = """ INSERT INTO SongTable (songName,ytLink) VALUES (?,?);"""
        db.execute(insertQ,item)
    con.commit()

if __name__ == '__main__':
    try:
        con = createCon()
        if not checkTables(con):
            createTables(con)
            print('Tables created')
    except sqlite3.Error as error:
        print('Error has occured', error)
    finally:
        if con:
            con.close()
            print('Connection terminated')