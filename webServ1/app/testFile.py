import setupDB
from sys import argv
import sqlite3

if __name__ == '__main__':
    try:
        con = setupDB.createCon()
        if not setupDB.checkTables(con):
            setupDB.createTables(con)
            print('Tables created')
        setupDB.addSongs(con)
    except sqlite3.Error as error:
        print('Error has occured', error)
    finally:
        if con:
            con.close()
            print('Connection terminated')