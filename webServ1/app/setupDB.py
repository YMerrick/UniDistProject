import sqlite3

#Checks if songs.db exist and if it does then checks if it contains information

#Connect to the database
def createCon(dfile='songs.db'):
    connection = sqlite3.connect(dfile)
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