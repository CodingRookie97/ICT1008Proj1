import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class FastestMRTGUI(QtWidgets.QMainWindow):
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

        lblFastestPathTitle = QLabel(self)
        lblFastestPathTitle.setText('Compute Fastest MRT Path')
        lblFastestPathTitle.setAlignment(Qt.AlignHCenter)
        lblFastestPathTitle.setFont(QFont("Arial", 20, QFont.Bold))
        lblFastestPathTitle.setStyleSheet('QLabel { color : Green; }')
        lblFastestPathTitle.adjustSize()
        titleLayout.addWidget(lblFastestPathTitle)

        gridLayout.addLayout(titleLayout, 0, 0)
        tableLayout = QtWidgets.QGridLayout(self.main)

        lblFastestMRT = QLabel(self)
        lblFastestMRT.setText('Fastest Path by MRT:')
        lblFastestMRT.setAlignment(Qt.AlignHCenter)
        lblFastestMRT.setFont(QFont("Arial", 14, QFont.Bold))
        lblFastestMRT.setStyleSheet('QLabel { color : Green; }')
        tableLayout.addWidget(lblFastestMRT, 1, 0)

        #print("Retrieved Path: " + str(self.path))
        #self.path = [swap(self.path[x]) for x in range(len(self.path))]
        nodeNames = []
        """with open('Combined/nodes.json') as f:
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
                                nodeNames.append(prop['node-details'])"""

        print(self.path)

        tableFastestBus = QTableWidget()
        tableFastestBus.setRowCount(len(self.path) + 1)
        tableFastestBus.setColumnCount(2)
        tableFastestBus.setItem(0, 0, QTableWidgetItem("Checkpoint Coordinates"))
        tableFastestBus.setItem(0, 1, QTableWidgetItem("Checkpoint Names"))
        """for i in range(len(self.path)):
            tableFastestBus.setItem(i + 1, 0, QTableWidgetItem(str(self.path[i])))
            tableFastestBus.setItem(i + 1, 1, QTableWidgetItem(str(nodeNames[i])))"""
        # Align columns to same width
        tableFastestBus.horizontalHeader().setStretchLastSection(True)
        tableFastestBus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set columns to read only, no editing
        tableFastestBus.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        tableLayout.addWidget(tableFastestBus, 3, 0)

        gridLayout.addLayout(tableLayout, 1, 0)

def swap(coord):
    return [coord[1], coord[0]]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fastest = FastestMRTGUI()
    sys.exit(app.exec_())