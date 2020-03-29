import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
import json

class DrivingPathGUI(QtWidgets.QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.title = 'ICT1008 AY19/20 Project Group 2-3'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.path = path
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

        self.main = QtWidgets.QWidget()
        self.setCentralWidget(self.main)
        gridLayout = QtWidgets.QGridLayout(self.main)

        titleLayout = QtWidgets.QHBoxLayout()

        lblShortestPathTitle = QLabel(self)
        lblShortestPathTitle.setText('Compute Shortest Path')
        lblShortestPathTitle.setAlignment(Qt.AlignHCenter)
        lblShortestPathTitle.setFont(QFont("Arial", 20, QFont.Bold))
        lblShortestPathTitle.setStyleSheet('QLabel { color : Green; }')
        lblShortestPathTitle.adjustSize()
        titleLayout.addWidget(lblShortestPathTitle)

        gridLayout.addLayout(titleLayout, 0, 0)
        tableLayout = QtWidgets.QGridLayout(self.main)

        lblShortestDrive = QLabel(self)
        lblShortestDrive.setText('Shortest Path by Driving:')
        lblShortestDrive.setAlignment(Qt.AlignHCenter)
        lblShortestDrive.setFont(QFont("Arial", 14, QFont.Bold))
        lblShortestDrive.setStyleSheet('QLabel { color : Red; }')
        tableLayout.addWidget(lblShortestDrive, 1, 0)

        self.path = [swap(self.path[x]) for x in range(len(self.path))]
        nodeNames = []

        with open('Combined/nodes.json') as f:
            getJson = json.load(f)
            feature_access = getJson['features']
            for feature_data in feature_access:
                prop = feature_data['properties']
                type = feature_data['geometry']['type']
                if type == 'Point':
                    coordinates = feature_data['geometry']['coordinates']
                    for i in range(len(self.path)):
                        if self.path[i] == coordinates:
                            if 'node-details' in prop:
                                nodeNames.append(prop['node-details'])

        with open('Combined/exportRoad.json') as f:
            getJson = json.load(f)
            feature_access = getJson['features']
            count = 0
            for feature_data in feature_access:
                type = feature_data['geometry']['type']
                if type == 'LineString':
                    coordinateList = feature_data['geometry']['coordinates']
                    for coordinate in coordinateList:
                        if isinstance(coordinate, list):
                            for i in range(len(self.path)):
                                if self.path[i] == coordinate:
                                    nodeNames.append(count)
                                    count += 1

        tableShortestDrive = QTableWidget()
        tableShortestDrive.setRowCount(len(self.path) + 1)
        tableShortestDrive.setColumnCount(2)
        tableShortestDrive.setItem(0, 0, QTableWidgetItem("Checkpoint Coordinates"))
        tableShortestDrive.setItem(0, 1, QTableWidgetItem("Checkpoint Names"))
        for i in range(len(self.path)):
            tableShortestDrive.setItem(i + 1, 0, QTableWidgetItem(str(self.path[i])))
            tableShortestDrive.setItem(i + 1, 1, QTableWidgetItem(str(nodeNames[i])))
        # Align columns to same width
        tableShortestDrive.horizontalHeader().setStretchLastSection(True)
        tableShortestDrive.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set columns to read only, no editing
        tableShortestDrive.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        tableLayout.addWidget(tableShortestDrive, 3, 0)
        gridLayout.addLayout(tableLayout, 1, 0)

def swap(coord):
    return [coord[1], coord[0]]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    driving = DrivingPathGUI()
    sys.exit(app.exec_())