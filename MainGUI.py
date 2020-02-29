import io
import sys

import folium

from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel


class MainGUI(QtWidgets.QMainWindow):
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
        bgImage = QImage("Images/punggol_background_1.png")
        sBgImage = bgImage.scaled(QSize(600, 400))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sBgImage))
        self.setPalette(palette)
        self.initWidgets()

    def initWidgets(self):
        #Initialise the main layout

        mrtStations = ["NE17/PTC Punggol MRT/LRT Station", "PW1 Sam Kee LRT Station", "PW2 Teck Lee LRT Station", "PW3 Punggol Point LRT Station", "PW4 Samudera LRT Station", "PW5 Nibong LRT Station", "PW6 Sumang LRT Station", "PW7 Soo Teck LRT Station"]
        residences = ["Punggol Regalia HDBs", "Punggol Arcadia HDBs", "Parc Centros HDBs", "Prive Condominiums", "Cornalius HDBs", "Treelodge at Punggol HDBs",
                                "Northshore Bungalows HDBs (U/C)", "Northshore Cove HDBs (U/C)", "Northshore StraitsView HDBs (U/C)", "Northshore Waterfront HDBs (U/C)", "Northshore Residences HDBs (U/C)",
                                "Northshore Edge HDBs", "Punggol Bayview HDBs", "Punggol Vue HDBs", "Piermont Grand Condominiums (U/C)", "ParcVista HDBs", "Waterway Terraces II HDBs",
                                "Waterway Cascadia HDBs", "Waterway Terraces I HDBs", "Punggol Opal HDBs", "Punggol Topaz HDBs", "Punggol Emerald HDBs", "Punggol Sapphire HDBs", "Punggol Residences HDBs"]

        self.main = QtWidgets.QWidget()
        self.setCentralWidget(self.main)
        gridLayout = QtWidgets.QGridLayout(self.main)

        #Combo Box Layout
        comboLayout = QtWidgets.QGridLayout(self.main)

        lblStartLocation = QLabel(self)
        lblStartLocation.setText('Choose a starting location:')
        lblStartLocation.setFont(QFont("Arial", 14, QFont.Bold))
        lblStartLocation.setStyleSheet('QLabel { color : Green; }')

        #Choose a start location (MRT station)
        self.comboStart = QComboBox()
        self.comboStart.addItems(mrtStations)
        self.comboStart.currentIndexChanged.connect(self.chooseStart)

        lblEndLocation = QLabel(self)
        lblEndLocation.setText('Choose a ending location:')
        lblEndLocation.setFont(QFont("Arial", 14, QFont.Bold))
        lblEndLocation.setStyleSheet('QLabel { color : Red; }')

        #Choose an ending location (Residential Estates HDB + Condominiums)
        self.comboEnd = QComboBox()
        self.comboEnd.addItems(residences)
        self.comboEnd.currentIndexChanged.connect(self.chooseEnd)

        #Adds widgets to the Combobox layout
        comboLayout.addWidget(lblStartLocation, 0, 0)
        comboLayout.addWidget(self.comboStart, 1, 0)
        comboLayout.addWidget(lblEndLocation, 0, 1)
        comboLayout.addWidget(self.comboEnd, 1, 1)
        gridLayout.addLayout(comboLayout, 0, 0)

        #Button to determine shortest path
        btnLayout = QtWidgets.QHBoxLayout()
        btnShortestPath = QtWidgets.QPushButton(self.tr("Compute shortest path"))
        btnShortestPath.setFont(QFont("Arial", 10, QFont.Bold))
        btnShortestPath.setStyleSheet('QPushButton { background-color: #008000; color: white; }')
        btnLayout.addWidget(btnShortestPath)
        gridLayout.addLayout(btnLayout, 1, 0)

        self.mapView = QtWebEngineWidgets.QWebEngineView()
        gridLayout.addWidget(self.mapView, 3, 0)
        gridLayout.setColumnStretch(1, 2)

        m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.mapView.setHtml(data.getvalue().decode())

    #Function to choose different starting locations
    def chooseStart(self, i):
        print("Current index", i, "selection changed ", self.comboStart.currentText())

    # Function to choose different ending locations
    def chooseEnd(self, i):
        print("Current index", i, "selection changed ", self.comboEnd.currentText())

if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainWindow = MainGUI()
    sys.exit(App.exec())