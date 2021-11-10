from sys import argv, exit
from PyQt5.QtWidgets import QApplication
import requests

class Client():
    def  __init__(self):
        pass

if __name__ == '__main__':
    app = QApplication(argv)
    window = Client()

    exit(app.exec_())