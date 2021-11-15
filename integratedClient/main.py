from sys import argv, exit
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QPushButton
import requests

class ArtistLife(QFrame):
    def __init__(self,name):
        super().__init__()
        self.setWindowTitle('About the Artist')
        text = QLabel(self.getArtistInfo(name))
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)

    #This is where the information about the artist is retrieved and returned as text
    def getArtistInfo(self,name):
        return name

class Client(QFrame):
    def  __init__(self):
        super().__init__()
        self.rSong = self.getSongOfTheDay()
        self.rArtist = self.getArtist(self.rSong['song'])

        self.setWindowTitle('Song of the day')
        button = QPushButton('About Artist')
        button.clicked.connect(self.artistButton)
        self.layout = QVBoxLayout()
        #QDesktopServices.openUrl(url=self.getSongLinkOfTheDay()['link'])
        link = self.createText()
        self.layout.addWidget(link)
        self.layout.addWidget(button)
        self.setLayout(self.layout)
        self.show()
        self.setMinimumSize(255,50)

    def artistButton(self):
        self.newW = ArtistLife(self.rArtist)
        self.newW.show()

    def createText(self):
        text = QLabel()
        text.setOpenExternalLinks(True)
        
        if self.rSong and self.rArtist:
            text.setText('<a href={0}>{1}</a>'.format(self.rSong['link'],self.rArtist+'- '+self.rSong['song']))
        else:
            text.setText('An error has occurred')
        return text

    def getSongOfTheDay(self):
        #Put a try catch block here to prevent crashes
        response = requests.get(url='http://127.0.0.1:5002/',timeout=2.5)
        if response.status_code != 404:
            song = response.json()
        else:
            return None
        response.close()
        return song

    def getSongLinkOfTheDay(self):
        #Put a try catch block here to prevent crashes
        response = requests.get(url='http://127.0.0.1:5000/link',timeout=2.5)
        if response.status_code == 404:
            return None
        else:
            link = response.json()
        response.close()
        return link

    def getArtist(self,songName):
        song = songName.replace(' ','_')
        response = requests.get(url='http://127.0.0.1:5000/song/'+song,timeout=2.5)
        if response.status_code == 404:
            return None
        elif response.status_code == 500:
            return None
        else:
            artist = response.text
        response.close()
        return artist.replace('"','')

    def get3rdWS(self):
        pass

if __name__ == '__main__':
    app = QApplication(argv)
    window = Client()

    exit(app.exec_())
