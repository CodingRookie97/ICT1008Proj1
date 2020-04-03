import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSlot, QSize

from MainGUI import MainGUI

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'ICT1008 AY19/20 Project Group 2-3'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('Images/punggol_logo.jpg'))

        bgImage = QImage("Images/punggol_background_1.png")
        sBgImage = bgImage.scaled(QSize(1100, 800))  # resize Image to fit the windows size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sBgImage))
        self.setPalette(palette)

        sitLogo = QLabel(self)
        pixmap = QPixmap.fromImage(QImage('Images/sit_logo.jpg').scaled(150, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        sitLogo.move(340, 20)
        sitLogo.setPixmap(pixmap.scaled(150, 120))

        lblGrpInfo = QLabel(self)
        lblGrpInfo.setText('ICT 1008 Project: Group 2-3')
        lblGrpInfo.setFont(QFont("Arial", 26, QFont.Bold))
        lblGrpInfo.setStyleSheet('QLabel { color : Blue; }')
        lblGrpInfo.move(240, 155)

        lblProjInfo = QLabel(self)
        lblProjInfo.setText('It\'s all about Punggol West!')
        lblProjInfo.setAlignment(Qt.AlignVCenter)
        lblProjInfo.setFont(QFont("Arial", 22, italic=True))
        lblProjInfo.setStyleSheet('QLabel { color : purple; }')
        lblProjInfo.move(270, 195)

        lblGrpNames = QLabel(self)
        lblGrpNames.setText('Team Members:\nOng Chang Hong\nJerone Poh Yong Cheng\nOng Kel Vyn\nChiu Jing Xiong\nEr Jayce')
        lblGrpNames.setFont(QFont("Arial", 22, QFont.Bold))
        lblGrpNames.setStyleSheet('QLabel { color : Blue; }')
        lblGrpNames.move(205, 230)

        lblGrpNames = QLabel(self)
        lblGrpNames.setText('Student ID:\n1902201\n1902606\n1902639\n1902669\n1902688')
        lblGrpNames.setAlignment(Qt.AlignHCenter)
        lblGrpNames.setFont(QFont("Arial", 22, QFont.Bold))
        lblGrpNames.setStyleSheet('QLabel { color : Red; }')
        lblGrpNames.move(485, 230)

        btnMainPage = QPushButton('Start Application', self)
        btnMainPage.setFont(QFont("Arial", 18, QFont.Bold))
        btnMainPage.setStyleSheet('QPushButton { background-color: #008000; color: white; }')
        btnMainPage.setToolTip('Click to start the application')
        btnMainPage.resize(380, 45)
        btnMainPage.move(205, 410)
        btnMainPage.clicked.connect(self.on_click)

        self.show()

    #Button click to enter main page
    @pyqtSlot()
    def on_click(self):
        self.toMain = MainGUI()
        self.toMain.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = App()
    sys.exit(app.exec_())