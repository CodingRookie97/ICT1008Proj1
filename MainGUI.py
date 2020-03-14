import io
import sys
import folium
import json

from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QCheckBox
from folium.plugins import MarkerCluster

from DrivingPathGUI import DrivingPathGUI
from FastestPathGUI import FastestPathGUI
from ShortestPathGUI import ShortestPathGUI

global mapView

#Initialise both starting and ending coordinates
startingCoordinates = None
endingCoordinates = None

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
        self.setWindowIcon(QIcon('Images/punggol_logo.jpg'))

        bgImage = QImage("Images/punggol_background_1.png")
        sBgImage = bgImage.scaled(QSize(1100, 800))  # resize Image to fit the windows size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sBgImage))
        self.setPalette(palette)
        self.initWidgets()

    def initWidgets(self):
        #Initialise the main layout
        self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
        self.marker_cluster = MarkerCluster().add_to(self.m)
        self.mapView = QtWebEngineWidgets.QWebEngineView()
        self.initMap(self.m, self.marker_cluster)

        #Array that contains the starting locations (Punggol West LRT Line only)
        mrtStations = ["NE17/PTC Punggol MRT/LRT Station", "PW1 Sam Kee LRT Station", "PW2 Teck Lee LRT Station", "PW3 Punggol Point LRT Station", "PW4 Samudera LRT Station", "PW5 Nibong LRT Station", "PW6 Sumang LRT Station", "PW7 Soo Teck LRT Station"]

        # Array that contains the ending locations (Those residential areas that cover Punggol West Area only)
        residences = self.importEnding('Buildings/residential_buildings.json')

        #Array that contains the mode of transport to compute shortest path
        mode = ["Walk", "Drive", "Bus", "Train (LRT/MRT)"]

        #Array that contains the bus services
        busServices = ["Bus 3", "Bus 34", "Bus 43", "Bus 43e", "Bus 43M", "Bus 50", "Bus 62", "Bus 82", "Bus 83", "Bus 84", "Bus 85", "Bus 117", "Bus 118", "Bus 119", "Bus 136", "Bus 381", "Bus 382G", "Bus 382W", "Bus 386"]

        self.main = QtWidgets.QWidget()
        self.setCentralWidget(self.main)
        gridLayout = QtWidgets.QGridLayout(self.main)

        #Combo Box Layout 1 for starting and ending location
        comboLayout1 = QtWidgets.QGridLayout(self.main)

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

        #Adds widgets to the Combobox layout for starting and ending location
        comboLayout1.addWidget(lblStartLocation, 0, 0)
        comboLayout1.addWidget(self.comboStart, 1, 0)
        comboLayout1.addWidget(lblEndLocation, 0, 1)
        comboLayout1.addWidget(self.comboEnd, 1, 1)
        gridLayout.addLayout(comboLayout1, 0, 0)

        #Button to determine shortest path + fastest Path
        btnLayout = QtWidgets.QGridLayout()
        btnShortestPath = QtWidgets.QPushButton(self.tr("Compute shortest walking path"))
        btnShortestPath.setFont(QFont("Arial", 10, QFont.Bold))
        btnShortestPath.setStyleSheet('QPushButton { background-color: #008000; color: white; }')
        btnLayout.addWidget(btnShortestPath, 0, 0)
        btnShortestPath.clicked.connect(self.computeShortest)

        btnDrivingPath = QtWidgets.QPushButton(self.tr("Compute shortest driving path"))
        btnDrivingPath.setFont(QFont("Arial", 10, QFont.Bold))
        btnDrivingPath.setStyleSheet('QPushButton { background-color: #FF8C00; color: white; }')
        btnLayout.addWidget(btnDrivingPath, 1, 0)
        btnDrivingPath.clicked.connect(self.computeDriving)

        btnFastestPath = QtWidgets.QPushButton(self.tr("Compute fastest bus/train path"))
        btnFastestPath.setFont(QFont("Arial", 10, QFont.Bold))
        btnFastestPath.setStyleSheet('QPushButton { background-color: #008B8B; color: white; }')
        btnFastestPath.clicked.connect(self.computeFastest)

        btnLayout.addWidget(btnFastestPath, 2, 0)
        gridLayout.addLayout(btnLayout, 1, 0)

        #Checkbox to select whether the bus routes are displayed on the map
        busLayout = QtWidgets.QGridLayout(self.main)
        lblBusRoutes = QLabel(self)
        lblBusRoutes.setText('Select a bus route to display on the map:')
        lblBusRoutes.setAlignment(Qt.AlignHCenter)
        lblBusRoutes.setFont(QFont("Arial", 14, QFont.Bold))
        lblBusRoutes.setStyleSheet('QLabel { color : Blue; }')

        busLayout.addWidget(lblBusRoutes, 0, 0)

        self.comboBusService = QComboBox(self)
        self.comboBusService.setFont(QFont("Arial", 10))
        self.comboBusService.addItems(busServices)
        self.comboBusService.currentIndexChanged.connect(self.chooseBus)
        busLayout.addWidget(self.comboBusService, 1, 0)

        btnSelectBus = QtWidgets.QPushButton(self.tr("Display Selected Bus Route"))
        btnSelectBus.setFont(QFont("Arial", 10, QFont.Bold))
        btnSelectBus.setStyleSheet('QPushButton { background-color: #800080; color: white; }')
        btnSelectBus.clicked.connect(self.selectBusService)
        busLayout.addWidget(btnSelectBus, 2, 0)

        self.lblSelectedBusRoute = QLabel(self)
        self.lblSelectedBusRoute.setText('Bus Route Displayed: ')
        self.lblSelectedBusRoute.setFont(QFont("Arial", 14, QFont.Bold))
        self.lblSelectedBusRoute.setStyleSheet('QLabel { color : Blue; }')

        busLayout.addWidget(self.lblSelectedBusRoute, 3, 0)

        gridLayout.addLayout(busLayout, 0, 2, 2, 1)

        #Layout to display the different types of legends of the map
        legendLayout = QtWidgets.QGridLayout()
        lblLegend = QLabel(self)
        lblLegend.setText('Legend:')
        lblLegend.setFont(QFont("Arial", 14, QFont.Bold))
        lblLegend.setStyleSheet('QLabel { color : #CC6600; }')
        legendLayout.addWidget(lblLegend, 0, 0)

        lrtLogo = QLabel(self)
        pixmapLRT = QPixmap.fromImage(QImage('Images/lrt_logo.png').scaled(20, 25, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        lrtLogo.setPixmap(pixmapLRT.scaled(20, 25))
        legendLayout.addWidget(lrtLogo, 1, 0)

        lblLRT = QLabel(self)
        lblLRT.setText('LRT Station')
        lblLRT.setFont(QFont("Arial", 12, QFont.Bold))
        lblLRT.setStyleSheet('QLabel { color : #5AB331; }')
        legendLayout.addWidget(lblLRT, 1, 1, 1, 2)

        busLogo = QLabel(self)
        pixmapBus = QPixmap.fromImage(QImage('Images/bus_stop_logo.png').scaled(20, 20, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        busLogo.setPixmap(pixmapBus.scaled(20, 20))
        legendLayout.addWidget(busLogo, 2, 0)

        lblBus = QLabel(self)
        lblBus.setText('Bus Stop')
        lblBus.setFont(QFont("Arial", 12, QFont.Bold))
        lblBus.setStyleSheet('QLabel { color : #1AA0E1; }')
        legendLayout.addWidget(lblBus, 2, 1, 1, 2)

        buildingLogo = QLabel(self)
        pixmapBuilding = QPixmap.fromImage(QImage('Images/building_logo.png').scaled(20, 20, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        buildingLogo.setPixmap(pixmapBuilding.scaled(20, 20))
        legendLayout.addWidget(buildingLogo, 3, 0)

        lblBuilding = QLabel(self)
        lblBuilding.setText('General Building')
        lblBuilding.setFont(QFont("Arial", 12, QFont.Bold))
        lblBuilding.setStyleSheet('QLabel { color : #FFA40B; }')
        legendLayout.addWidget(lblBuilding, 3, 1, 1, 2)

        houseLogo = QLabel(self)
        pixmapBuilding = QPixmap.fromImage(QImage('Images/home_logo.png').scaled(20, 20, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        houseLogo.setPixmap(pixmapBuilding.scaled(20, 20))
        legendLayout.addWidget(houseLogo, 4, 0)

        lblHouse = QLabel(self)
        lblHouse.setText('Residential Housing')
        lblHouse.setFont(QFont("Arial", 12, QFont.Bold))
        lblHouse.setStyleSheet('QLabel { color : #6782A4; }')
        legendLayout.addWidget(lblHouse, 4, 1, 1, 2)

        gridLayout.addLayout(legendLayout, 2, 2, 1, 1)

        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.mapView.setHtml(data.getvalue().decode())
        gridLayout.addWidget(self.mapView, 2, 0, 2, 1)

    def importEnding(self, file):
        ending = []
        with open(file) as f:
            self.getJson = json.load(f)
        feature_access = self.getJson['features']
        #retrieve and populate the names of the nodes from json file
        for feature_data in feature_access:
            ending.append(feature_data['properties']['node-details'])
        return ending

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

    def importAreaOfInterest(self, file, map):
        with open(file) as f:
            self.getJson = json.load(f)
        feature_access = self.getJson['features']
        coordinates = [[]]
        for feature_data in feature_access:
            coordinates = feature_data['geometry']['coordinates']
            for c in coordinates:
                c[0], c[1] = c[1], c[0]
        folium.PolyLine(coordinates, color="blue", weight=3).add_to(map)

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

    def chooseBus(self, i):
        print("Current index", i, "selection changed ", self.comboBusService.currentText())

    #Function to choose different bus service to display on the map
    def selectBusService(self):
        self.lblSelectedBusRoute.setText('Bus Route Displayed: ' + self.comboBusService.currentText())
        if self.comboBusService.currentText() == "Bus 3":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus3/Bus_3_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus3/Bus_3_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 34":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus34/Bus_34_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus34/Bus_34_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 43":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus43/Bus_43_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus43/Bus_43_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 43e":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus43/Bus_43E_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus43/Bus_43E_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 43M":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus43/Bus_43M_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus43/Bus_43M_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 50":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus50/Bus_50_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus50/Bus_50_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 62":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus62/Bus_62_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus62/Bus_62_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 82":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus82/Bus_82_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus82/Bus_82_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 83":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus83/Bus_83_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus83/Bus_83_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 84":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus84/Bus_84.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 85":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus85/Bus_85_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
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
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 117":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus117/Bus_117_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus117/Bus_117_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 118":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus118/Bus_118_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus118/Bus_118_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 119":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus119/Bus_119_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus119/Bus_119_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 136":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus136/Bus_136_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus136/Bus_136_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 381":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus381/Bus_381_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus381/Bus_381_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 382G":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus382/Bus_382G.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 382W":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus382/Bus_382W.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

        if self.comboBusService.currentText() == "Bus 386":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus386/Bus_386_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="green", weight=3).add_to(self.m)
            coordinates = [[]]
            with open("Bus_Services/Bus386/Bus_386_to.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="red", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

    @pyqtSlot()
    def computeShortest(self):
        #TODO: Insert shortest path algorithm here
        #self.shortestPath = ShortestPathGUI(self.comboStart.currentText(), self.comboEnd.currentText())
        #self.shortestPath.show()


        pass

    @pyqtSlot()
    def computeDriving(self):
        #TODO: Insert shortest driving path algorithm here
        #self.drivingPath = DrivingPathGUI(self.comboStart.currentText(), self.comboEnd.currentText())
        #self.drivingPath.show()
        pass

    @pyqtSlot()
    def computeFastest(self):
        #TODO: Insert fastest train path algorithm here
        #elf.fastestPath = FastestPathGUI(self.comboStart.currentText(), self.comboEnd.currentText())
        #self.fastestPath.show()
        pass

if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainWindow = MainGUI()
    sys.exit(App.exec_())