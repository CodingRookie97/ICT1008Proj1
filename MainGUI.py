import io
import os
import sys
from collections import OrderedDict
from haversine import haversine

import folium
import json

from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel
from folium.plugins import MarkerCluster

from ShortestPathGUI import ShortestPathGUI

from ShortestPath import ShortestPath

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

        # Array that contains the ending locations (Those residential areas that cover Punggol West Area only)
        startEndingLocation = self.importStartEnding('Combined/nodes.json')

        #Array that contains the bus services
        busServices = ["Bus 3", "Bus 34", "Bus 43", "Bus 50", "Bus 62", "Bus 82", "Bus 83", "Bus 84", "Bus 85", "Bus 117", "Bus 118", "Bus 119", "Bus 136", "Bus 381", "Bus 382G", "Bus 382W", "Bus 386"]

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
        self.comboStart.addItems(startEndingLocation)
        self.comboStart.currentIndexChanged.connect(self.chooseStart)

        lblEndLocation = QLabel(self)
        lblEndLocation.setText('Choose ending location:')
        lblEndLocation.setFont(QFont("Arial", 14, QFont.Bold))
        lblEndLocation.setStyleSheet('QLabel { color : Red; }')

        #Choose an ending location (Residential Estates HDB + Condominiums)
        self.comboEnd = QComboBox()
        self.comboEnd.setFont(QFont("Arial", 10))
        self.comboEnd.addItems(startEndingLocation)
        self.comboEnd.currentIndexChanged.connect(self.chooseEnd)

        #Adds widgets to the Combobox layout for starting and ending location
        comboLayout1.addWidget(lblStartLocation, 0, 0)
        comboLayout1.addWidget(self.comboStart, 1, 0)
        comboLayout1.addWidget(lblEndLocation, 0, 1)
        comboLayout1.addWidget(self.comboEnd, 1, 1)
        gridLayout.addLayout(comboLayout1, 0, 0)

        #Button to determine shortest path + fastest Path
        btnLayout = QtWidgets.QGridLayout()
        btnWalkingPath = QtWidgets.QPushButton(self.tr("Compute shortest walking path"))
        btnWalkingPath.setFont(QFont("Arial", 10, QFont.Bold))
        btnWalkingPath.setStyleSheet('QPushButton { background-color: #008000; color: white; }')
        btnLayout.addWidget(btnWalkingPath , 0, 0)
        btnWalkingPath.clicked.connect(self.computeWalking)

        btnFastestBusPath = QtWidgets.QPushButton(self.tr("Compute fastest bus path"))
        btnFastestBusPath.setFont(QFont("Arial", 10, QFont.Bold))
        btnFastestBusPath.setStyleSheet('QPushButton { background-color: #008B8B; color: white; }')
        btnFastestBusPath.clicked.connect(self.computeFastestBus)
        btnLayout.addWidget(btnFastestBusPath, 1, 0)

        btnFastestTrainPath = QtWidgets.QPushButton(self.tr("Compute fastest train path"))
        btnFastestTrainPath.setFont(QFont("Arial", 10, QFont.Bold))
        btnFastestTrainPath.setStyleSheet('QPushButton { background-color: #FF0000; color: white; }')
        btnFastestTrainPath.clicked.connect(self.computeFastestTrain)
        btnLayout.addWidget(btnFastestTrainPath, 2, 0)
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

    def importStartEnding(self, file):
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
            with open("Bus_Services/Bus_3_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 34":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_34_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 43":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_43_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 50":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_50_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 62":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_62_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 82":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_82_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 83":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_83_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 84":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_84.json") as f:
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
            with open("Bus_Services/Bus_85_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 117":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_117_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 118":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_118_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 119":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_119_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 136":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_136_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 381":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_381_from.json") as f:
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

        if self.comboBusService.currentText() == "Bus 382G":
            coordinates = [[]]
            self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
            with open("Bus_Services/Bus_382G.json") as f:
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
            with open("Bus_Services/Bus_382W.json") as f:
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
            with open("Bus_Services/Bus_386_from.json") as f:
                getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinates = feature_data['geometry']['coordinates']
                    for c in coordinates:
                        c[0], c[1] = c[1], c[0]
            folium.PolyLine(coordinates, color="#800080", weight=3).add_to(self.m)
            self.marker_cluster = MarkerCluster().add_to(self.m)
            self.initMap(self.m, self.marker_cluster)
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.mapView.setHtml(data.getvalue().decode())

    @pyqtSlot()
    def computeWalking(self):
        nodes = {}
        with open('Combined/nodes.json') as f:
            getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                prop = feature_data['properties']
                if 'node-details' in prop:
                    location_name = prop['node-details']
                    nodes[location_name] = feature_data['geometry']['coordinates']

        pathfinder = ShortestPath(nodes)
        pathfinder.create_edges()
        graph = pathfinder.build_graph()
        path = pathfinder.find_shortest_path(graph, self.comboStart.currentText(), self.comboEnd.currentText())
        folium.PolyLine(path, color="#008000", weight=3).add_to(self.m)
        self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
        self.lblSelectedBusRoute.setText('Bus Route Displayed: ')
        folium.PolyLine(path, opacity=1, color='green').add_to(self.m)
        self.marker_cluster = MarkerCluster().add_to(self.m)
        self.initMap(self.m, self.marker_cluster)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.mapView.setHtml(data.getvalue().decode())

        self.walkingPath = ShortestPathGUI(path)
        self.walkingPath.show()

    @pyqtSlot()
    def computeFastestBus(self):
        # Fastest Bus Route
        nodes = OrderedDict()
        edges = []
        busPath = []
        busRoutes = OrderedDict()
        busNodes = {}
        temp = {}
        filedir = "Bus_Path\\"
        json_files = [pos_json for pos_json in os.listdir(filedir) if pos_json.endswith('.geojson')]
        for f in json_files:
            with open(filedir + f) as json_file:
                data = json.load(json_file)

            for feature in data['features']:

                if feature['geometry']['type'] == 'MultiLineString':
                    for y in feature['geometry']['coordinates']:
                        busPath.append(y)

                else:
                    coord = feature['geometry']['coordinates']
                    nodes[feature['properties']['node-details']] = coord
                    print("Nodes: " + str(coord))
                    busNodes[tuple(coord)] = feature['properties']['node-details']

                    lowest = 999
                    lowestIndex = 0
                    for i in range(len(busPath)):
                        print(busPath[i])
                        d = haversine(coord, busPath[i])
                        if d < lowest:
                            lowest = d
                            lowestIndex = i
                    busPath.insert(lowestIndex, coord)

            length = len(busPath)
            for i in range(length):
                c = tuple(busPath[i])
                k = str(i)
                busRoutes[k] = c
                temp[c] = k

            # complete dictionary

            for i in range(length):
                if i + 1 != length:
                    d = haversine(busPath[i], busPath[i + 1])
                    if tuple(busPath[i]) in busNodes:
                        edges.append((busNodes[tuple(busPath[i])], temp[tuple(busPath[i + 1])], d / 60, "Bus"))
                    elif tuple(busPath[i + 1]) in busNodes:
                        edges.append((temp[tuple(busPath[i])], busNodes[tuple(busPath[i + 1])], d / 60, "Bus"))
                    else:
                        edges.append((temp[tuple(busPath[i])], temp[tuple(busPath[i + 1])], d / 60, "Bus"))

            temp.clear()
            busPath.clear()

        with open('Combined/nodes.json') as f:
            getJson = json.load(f)
            feature_access = getJson['features']

            for feature_data in feature_access:
                prop = feature_data['properties']
                if 'node-details' in prop:
                    location_name = prop['node-details']
                    nodes[location_name] = feature_data['geometry']['coordinates']

        pathfinder = ShortestPath(nodes)
        pathfinder.create_edges()
        pathfinder.create_bus_edgenodes(edges, busNodes, busRoutes)
        graph = pathfinder.build_graph()
        print("Get graph: " + str(graph))
        path = pathfinder.find_shortest_path(graph, self.comboStart.currentText(), self.comboEnd.currentText())

        print("Get Path: " + str(path))

        self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
        self.lblSelectedBusRoute.setText('Bus Route Displayed: ')
        folium.PolyLine(path, opacity=1, color='#800080').add_to(self.m)
        self.marker_cluster = MarkerCluster().add_to(self.m)
        self.initMap(self.m, self.marker_cluster)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.mapView.setHtml(data.getvalue().decode())

    @pyqtSlot()
    def computeFastestTrain(self):
        nodes = OrderedDict()
        edges = []
        mrtPath = []
        mrtRoutes = OrderedDict()
        mrtNodes = {}
        temp = {}
        filedir = "MRT\\"
        json_files = [pos_json for pos_json in os.listdir(filedir) if pos_json.endswith('.geojson')]
        for f in json_files:
            with open(filedir + f) as json_file:
                data = json.load(json_file)

            for feature in data['features']:

                if feature['geometry']['type'] == 'MultiLineString':
                    for y in feature['geometry']['coordinates']:
                        mrtPath.append(y)

                else:
                    coord = feature['geometry']['coordinates']
                    nodes[feature['properties']['node-details']] = coord
                    mrtNodes[tuple(coord)] = feature['properties']['node-details']

                    lowest = 999
                    lowestIndex = 0
                    for i in range(len(mrtPath)):
                        print(mrtPath[i])
                        d = haversine(coord, mrtPath[i])
                        if d < lowest:
                            lowest = d
                            lowestIndex = i
                    mrtPath.insert(lowestIndex, coord)

            length = len(mrtPath)
            for i in range(length):
                c = tuple(mrtPath[i])
                k = str(i)
                mrtRoutes[k] = c
                temp[c] = k

            # complete dictionary

            for i in range(length):
                if i + 1 != length:
                    d = haversine(mrtPath[i], mrtPath[i + 1])
                    if tuple(mrtPath[i]) in mrtNodes:
                        edges.append((mrtNodes[tuple(mrtPath[i])], temp[tuple(mrtPath[i + 1])], d / 70, "LRT"))
                    elif tuple(mrtPath[i + 1]) in mrtNodes:
                        edges.append((temp[tuple(mrtPath[i])], mrtNodes[tuple(mrtPath[i + 1])], d / 70, "LRT"))
                    else:
                        edges.append((temp[tuple(mrtPath[i])], temp[tuple(mrtPath[i + 1])], d / 70, "LRT"))

            temp.clear()
            mrtPath.clear()

        with open('Combined/nodes.json') as f:
            getJson = json.load(f)
            feature_access = getJson['features']

            for feature_data in feature_access:
                prop = feature_data['properties']
                if 'node-details' in prop:
                    location_name = prop['node-details']
                    nodes[location_name] = feature_data['geometry']['coordinates']

        pathfinder = ShortestPath(nodes)
        pathfinder.create_edges()
        pathfinder.create_mrt_edgenodes(edges, mrtNodes, mrtRoutes)
        graph = pathfinder.build_graph()
        print("Get graph: " + str(graph))
        path = pathfinder.find_shortest_path(graph, self.comboStart.currentText(), self.comboEnd.currentText())

        print("Get Path: " + str(path))

        self.m = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
        self.lblSelectedBusRoute.setText('Bus Route Displayed: ')
        folium.PolyLine(path, opacity=1, color='red').add_to(self.m)
        self.marker_cluster = MarkerCluster().add_to(self.m)
        self.initMap(self.m, self.marker_cluster)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.mapView.setHtml(data.getvalue().decode())

if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainWindow = MainGUI()
    sys.exit(App.exec_())