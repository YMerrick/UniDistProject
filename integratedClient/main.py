from sys import argv, exit
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel
from PyQt5.QtGui import QDesktopServices
import requests

class Client(QFrame):
    def  __init__(self):
        super().__init__()
        self.setWindowTitle('Song of the day')
        self.layout = QVBoxLayout()
        #QDesktopServices.openUrl(url=self.getSongLinkOfTheDay()['link'])
        self.link = QLabel()
        self.link.setOpenExternalLinks(True)
        response = self.getSongOfTheDay()
        self.link.setText('<a href={0}>{1}</a>'.format(response['link'],response['song']))
        self.layout.addWidget(self.link)
        self.setLayout(self.layout)
        self.show()

    def getSongOfTheDay(self):
        #Put a try catch block here to prevent crashes
        response = requests.get(url='http://127.0.0.1:5000/')
        song = response.json()
        response.close()
        return song
    
    def getSongLinkOfTheDay(self):
        #Put a try catch block here to prevent crashes
        response = requests.get(url='http://127.0.0.1:5000/link')
        link = response.json()
        response.close()
        return link

    def getArtist(self):
        pass

if __name__ == '__main__':
    app = QApplication(argv)
    window = Client()

    exit(app.exec_())
