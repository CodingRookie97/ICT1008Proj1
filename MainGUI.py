import io
import sys
import folium
import json

from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QCheckBox
from folium.plugins import MarkerCluster

from ShortestPathGUI import ShortestPathGUI

m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
marker_cluster = MarkerCluster().add_to(m)

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
        sBgImage = bgImage.scaled(QSize(800, 600))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sBgImage))
        self.setPalette(palette)
        self.initWidgets()

    def initWidgets(self):
        #Initialise the main layout

        mapView = QtWebEngineWidgets.QWebEngineView()
        self.initMap(m, marker_cluster)

        #Array that contains the starting locations (Punggol West LRT Line only)
        mrtStations = ["NE17/PTC Punggol MRT/LRT Station", "PW1 Sam Kee LRT Station", "PW2 Teck Lee LRT Station", "PW3 Punggol Point LRT Station", "PW4 Samudera LRT Station", "PW5 Nibong LRT Station", "PW6 Sumang LRT Station", "PW7 Soo Teck LRT Station"]

        # Array that contains the ending locations (Those residential areas that cover Punggol West Area only)
        residences = ["Punggol Regalia HDBs", "Punggol Arcadia HDBs", "Parc Centros HDBs", "Prive Condominiums", "Cornalius HDBs", "Treelodge at Punggol HDBs",
                    "Northshore Bungalows", "Punggol Point Woods HDBs (U/C)", "Punggol Point Cove HDBs (U/C)", "Punggol Point Crown HDBs (U/C)", "NorthShore Trio HDBs (U/C)", "Northshore Cove HDBs (U/C)", "Northshore StraitsView HDBs (U/C)",
                      "Northshore Waterfront HDBs (U/C)", "Northshore Residences HDBs (U/C)",  "Northshore Edge HDBs (U/C)", "Punggol Bayview HDBs", "Punggol Vue HDBs", "Piermont Grand Condominiums (U/C)",
                      "ParcVista HDBs", "Waterway Terraces II HDBs", "Waterway Cascadia HDBs", "Waterway Terraces I HDBs", "Punggol Opal HDBs", "Punggol Topaz HDBs", "Punggol Emerald HDBs", "Punggol Sapphire HDBs", "Punggol Residences HDBs"]

        self.main = QtWidgets.QWidget()
        self.setCentralWidget(self.main)
        gridLayout = QtWidgets.QGridLayout(self.main)

        #Combo Box Layout
        comboLayout = QtWidgets.QGridLayout(self.main)

        lblStartLocation = QLabel(self)
        lblStartLocation.setText('Choose starting location:')
        lblStartLocation.setFont(QFont("Arial", 14, QFont.Bold))
        lblStartLocation.setStyleSheet('QLabel { color : Green; }')

        #Choose a start location (MRT station)
        self.comboStart = QComboBox()
        self.comboStart.setFont(QFont("Arial", 10))
        self.comboStart.addItems(mrtStations)
        self.comboStart.currentIndexChanged.connect(self.chooseStart)

        lblEndLocation = QLabel(self)
        lblEndLocation.setText('Choose ending location:')
        lblEndLocation.setFont(QFont("Arial", 14, QFont.Bold))
        lblEndLocation.setStyleSheet('QLabel { color : Red; }')

        #Choose an ending location (Residential Estates HDB + Condominiums)
        self.comboEnd = QComboBox()
        self.comboEnd.setFont(QFont("Arial", 10))
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
        btnShortestPath.clicked.connect(self.computeShortest)
        gridLayout.addLayout(btnLayout, 1, 0)

        gridLayout.addWidget(mapView, 2, 0)

        data = io.BytesIO()
        m.save(data, close_file=False)
        mapView.setHtml(data.getvalue().decode())

        #Checkbox to select whether the bus routes are displayed on the map
        lblChkBoxLayout = QtWidgets.QGridLayout(self.main)

        lblCheckBusRoutes = QLabel(self)
        lblCheckBusRoutes.setText('Check to display bus routes on the map:')
        lblCheckBusRoutes.setAlignment(Qt.AlignHCenter)
        lblCheckBusRoutes.setFont(QFont("Arial", 14, QFont.Bold))
        lblCheckBusRoutes.setStyleSheet('QLabel { color : Blue; }')
        lblChkBoxLayout.addWidget(lblCheckBusRoutes, 0, 0)
        gridLayout.addLayout(lblChkBoxLayout, 1, 4)

        cbBus3 = QCheckBox("Bus 3", self)
        cbBus3.stateChanged.connect(self.checkBus3)
        cbBus3.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus34 = QCheckBox("Bus 34", self)
        cbBus34.stateChanged.connect(self.checkBus34)
        cbBus34.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus43 = QCheckBox("Bus 43", self)
        cbBus43.stateChanged.connect(self.checkBus43)
        cbBus43.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus43e = QCheckBox("Bus 43e", self)
        cbBus43e.stateChanged.connect(self.checkBus43e)
        cbBus43e.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus43M = QCheckBox("Bus 43M", self)
        cbBus43M.stateChanged.connect(self.checkBus43M)
        cbBus43M.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus50 = QCheckBox("Bus 50", self)
        cbBus50.stateChanged.connect(self.checkBus50)
        cbBus50.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus62 = QCheckBox("Bus 62", self)
        cbBus62.stateChanged.connect(self.checkBus62)
        cbBus62.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus82 = QCheckBox("Bus 82", self)
        cbBus82.stateChanged.connect(self.checkBus82)
        cbBus82.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus83 = QCheckBox("Bus 83", self)
        cbBus83.stateChanged.connect(self.checkBus83)
        cbBus83.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus84 = QCheckBox("Bus 84", self)
        cbBus84.stateChanged.connect(self.checkBus84)
        cbBus84.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus85 = QCheckBox("Bus 85", self)
        cbBus85.stateChanged.connect(self.checkBus85)
        cbBus85.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus117 = QCheckBox("Bus 117", self)
        cbBus117.stateChanged.connect(self.checkBus117)
        cbBus117.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus118 = QCheckBox("Bus 118", self)
        cbBus118.stateChanged.connect(self.checkBus118)
        cbBus118.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus119 = QCheckBox("Bus 119", self)
        cbBus119.stateChanged.connect(self.checkBus119)
        cbBus119.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus136 = QCheckBox("Bus 136", self)
        cbBus136.stateChanged.connect(self.checkBus136)
        cbBus136.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus381 = QCheckBox("Bus 381", self)
        cbBus381.stateChanged.connect(self.checkBus381)
        cbBus381.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus382G = QCheckBox("Bus 382G", self)
        cbBus382G.stateChanged.connect(self.checkBus382G)
        cbBus382G.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus382W = QCheckBox("Bus 382W", self)
        cbBus382W.stateChanged.connect(self.checkBus382W)
        cbBus382W.setFont(QFont("Arial", 10, QFont.Bold))

        cbBus386 = QCheckBox("Bus 386", self)
        cbBus386.stateChanged.connect(self.checkBus386)
        cbBus386.setFont(QFont("Arial", 10, QFont.Bold))

        chkBoxLayout = QtWidgets.QGridLayout(self.main)
        chkBoxLayout.addWidget(cbBus3, 0, 0)
        chkBoxLayout.addWidget(cbBus34, 0, 1)
        chkBoxLayout.addWidget(cbBus43, 0, 2)
        chkBoxLayout.addWidget(cbBus43e, 1, 0)
        chkBoxLayout.addWidget(cbBus43M, 1, 1)
        chkBoxLayout.addWidget(cbBus50, 1, 2)
        chkBoxLayout.addWidget(cbBus62, 2, 0)
        chkBoxLayout.addWidget(cbBus82, 2, 1)
        chkBoxLayout.addWidget(cbBus83, 2, 2)
        chkBoxLayout.addWidget(cbBus84, 3, 0)
        chkBoxLayout.addWidget(cbBus85, 3, 1)
        chkBoxLayout.addWidget(cbBus117, 3, 2)
        chkBoxLayout.addWidget(cbBus118, 4, 0)
        chkBoxLayout.addWidget(cbBus119, 4, 1)
        chkBoxLayout.addWidget(cbBus136, 4, 2)
        chkBoxLayout.addWidget(cbBus381, 5, 0)
        chkBoxLayout.addWidget(cbBus382G, 5, 1)
        chkBoxLayout.addWidget(cbBus382W, 5, 2)
        chkBoxLayout.addWidget(cbBus386, 6, 1)
        gridLayout.addLayout(chkBoxLayout, 2, 4)

    def initMap(self, map, markerCluster):
        #This is to import the area of interest polyline from json file to display on folium map
        self.importAreaOfInterest('Combined/area_of_interest.json', map)
        #This is to import the train stations from json file to display on folium map (starting location)
        self.importTrainStns('MRT/mrt.json', markerCluster)
        #This is to import the bus stops from json file to display on folium map
        self.importBusStops('Bus_Stops/bus_stops.json', map)
        #This is to import the general buildings from json file to display on folium map
        self.importBuildings('Buildings/general_buildings.json', map)
        # This is to import the residential buildings from json file to display on folium map (ending location)
        self.importResidential('Buildings/residential_buildings.json', map)

        coordinates = [[]]
        with open("Bus_Services/Bus85/Bus_85_from.json") as f:
            getJson = json.load(f)
        feature_access = getJson['features']
        for feature_data in feature_access:
            type = feature_data['geometry']['type']
            if type == 'LineString':
                coordinates = feature_data['geometry']['coordinates']
                for c in coordinates:
                    c[0], c[1] = c[1], c[0]
        folium.PolyLine(coordinates, color="blue", weight=3).add_to(m)
        coordinates = [[]]
        with open("Bus_Services/Bus85/Bus_85_to.json") as f:
            getJson = json.load(f)
        feature_access = getJson['features']
        for feature_data in feature_access:
            type = feature_data['geometry']['type']
            if type == 'LineString':
                coordinates = feature_data['geometry']['coordinates']
                for c in coordinates:
                    c[0], c[1] = c[1], c[0]
        folium.PolyLine(coordinates, color="orange", weight=3).add_to(m)

    def importAreaOfInterest(self, file, map):
        with open(file) as f:
            self.getJson = json.load(f)
        feature_access = self.getJson['features']
        coordinates = [[]]
        for feature_data in feature_access:
            coordinates = feature_data['geometry']['coordinates']
            for c in coordinates:
                c[0], c[1] = c[1], c[0]
        folium.PolyLine(coordinates, color="red", weight=3).add_to(map)

    def importTrainStns(self, file, markerCluster):
        with open(file) as f:
            self.getJson = json.load(f)
        feature_access = self.getJson['features']
        for feature_data in feature_access:
            prop = feature_data['properties']
            coordinates = feature_data['geometry']['coordinates']
            coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
            icon = folium.features.CustomIcon('Images/lrt_logo.png', icon_size=(20, 25))
            folium.Marker(coordinates, popup=prop['node-details'], icon=icon).add_to(markerCluster)

    def importBusStops(self, file, map):
        with open(file) as f:
            self.getJson = json.load(f)
        feature_access = self.getJson['features']
        for feature_data in feature_access:
            prop = feature_data['properties']
            coordinates = feature_data['geometry']['coordinates']
            coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
            icon = folium.features.CustomIcon('Images/bus_stop_logo.png', icon_size=(20, 20))
            folium.Marker(coordinates, popup=prop['node-details'], icon=icon).add_to(map)

    def importBuildings(self, file, map):
        with open(file) as f:
            self.getJson = json.load(f)
        feature_access = self.getJson['features']
        for feature_data in feature_access:
            prop = feature_data['properties']
            coordinates = feature_data['geometry']['coordinates']
            coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
            icon = folium.features.CustomIcon('Images/building_logo.png', icon_size=(20, 20))
            folium.Marker(coordinates, popup=prop['node-details'], icon=icon).add_to(map)

    def importResidential(self, file, map):
        with open(file) as f:
            self.getJson = json.load(f)
        feature_access = self.getJson['features']
        for feature_data in feature_access:
            prop = feature_data['properties']
            coordinates = feature_data['geometry']['coordinates']
            coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
            icon = folium.features.CustomIcon('Images/home_logo.png', icon_size=(20, 20))
            folium.Marker(coordinates, popup=prop['node-details'], icon=icon).add_to(map)

    #Function to choose different starting locations
    def chooseStart(self, i):
        print("Current index", i, "selection changed ", self.comboStart.currentText())

    #Function to choose different ending locations
    def chooseEnd(self, i):
        print("Current index", i, "selection changed ", self.comboEnd.currentText())

    #Function to disable/enable the showing of bus routes in the map
    def checkBus3(self, state):
        if state == Qt.Checked:
            print('Bus 3 Checked')
        else:
            print('Bus 3 Unchecked')

    def checkBus34(self, state):
        if state == Qt.Checked:
            print('Bus 34 Checked')
        else:
            print('Bus 34 Unchecked')

    def checkBus43(self, state):
        if state == Qt.Checked:
            print('Bus 43 Checked')
        else:
            print('Bus 43 Unchecked')

    def checkBus43e(self, state):
        if state == Qt.Checked:
            print('Bus 43e Checked')
        else:
            print('Bus 43e Unchecked')

    def checkBus43M(self, state):
        if state == Qt.Checked:
            print('Bus 43M Checked')
        else:
            print('Bus 43M Unchecked')

    def checkBus50(self, state):
        if state == Qt.Checked:
            print('Bus 50 Checked')
        else:
            print('Bus 50 Unchecked')

    def checkBus62(self, state):
        if state == Qt.Checked:
            print('Bus 62 Checked')
        else:
            print('Bus 62 Unchecked')

    def checkBus82(self, state):
        if state == Qt.Checked:
            print('Bus 82 Checked')
        else:
            print('Bus 82 Unchecked')

    def checkBus83(self, state):
        if state == Qt.Checked:
            print('Bus 83 Checked')
        else:
            print('Bus 83 Unchecked')

    def checkBus84(self, state):
        if state == Qt.Checked:
            print('Bus 84 Checked')
        else:
            print('Bus 84 Unchecked')

    def checkBus85(self, state):
        if state == Qt.Checked:
            print('Bus 85 Checked')
        else:
            print('Bus 85 Unchecked')

    def checkBus117(self, state):
        if state == Qt.Checked:
            print('Bus 117 Checked')
        else:
            print('Bus 117 Unchecked')

    def checkBus118(self, state):
        if state == Qt.Checked:
            print('Bus 118 Checked')
        else:
            print('Bus 118 Unchecked')

    def checkBus119(self, state):
        if state == Qt.Checked:
            print('Bus 119 Checked')
        else:
            print('Bus 119 Unchecked')

    def checkBus136(self, state):
        if state == Qt.Checked:
            print('Bus 136 Checked')
        else:
            print('Bus 136 Unchecked')

    def checkBus381(self, state):
        if state == Qt.Checked:
            print('Bus 381 Checked')
        else:
            print('Bus 381 Unchecked')

    def checkBus382G(self, state):
        if state == Qt.Checked:
            print('Bus 382G Checked')
        else:
            print('Bus 382G Unchecked')

    def checkBus382W(self, state):
        if state == Qt.Checked:
            print('Bus 382W Checked')
        else:
            print('Bus 382W Unchecked')

    def checkBus386(self, state):
        if state == Qt.Checked:
            print('Bus 386 Checked')
        else:
            print('Bus 386 Unchecked')

    @pyqtSlot()
    def computeShortest(self):
        #TODO: Insert shortest path algorithm here
        self.shortestPath = ShortestPathGUI(self.comboStart.currentText(), self.comboEnd.currentText())
        self.shortestPath.show()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainWindow = MainGUI()
    sys.exit(App.exec_())