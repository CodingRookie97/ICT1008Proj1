import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class ShortestPathGUI(QtWidgets.QMainWindow):
    def __init__(self, startLocation, endLocation, mode):
        super().__init__()
        self.title = 'ICT1008 AY19/20 Project Group 2-3'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.mode = mode
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('Images/punggol_logo.jpg'))

        bgImage = QImage("Images/punggol_background_1.png")
        sBgImage = bgImage.scaled(QSize(800, 600))  # resize Image to widgets size
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

        if (self.mode == "Walk"):
            lblWalkDistance = QLabel(self)
            lblWalkDistance.setText('Total Walking Distance:')
            lblWalkDistance.setFont(QFont("Arial", 14, QFont.Bold))
            lblWalkDistance.setStyleSheet('QLabel { color : Blue; }')
            tableLayout.addWidget(lblWalkDistance, 1, 0)

            lblShortestWalk = QLabel(self)
            lblShortestWalk.setText('Shortest Path by Walking:')
            lblShortestWalk.setAlignment(Qt.AlignHCenter)
            lblShortestWalk.setFont(QFont("Arial", 14, QFont.Bold))
            lblShortestWalk.setStyleSheet('QLabel { color : Orange; }')
            tableLayout.addWidget(lblShortestWalk, 2, 0)

            tableShortestWalk = QTableWidget()
            tableShortestWalk.setRowCount(20)
            tableShortestWalk.setColumnCount(5)
            tableShortestWalk.setItem(0, 0, QTableWidgetItem("Starting Node"))
            tableShortestWalk.setItem(0, 1, QTableWidgetItem("Target Node"))
            tableShortestWalk.setItem(0, 2, QTableWidgetItem("Cost"))
            tableShortestWalk.setItem(0, 3, QTableWidgetItem("Estimated time taken to reach"))
            tableShortestWalk.setItem(0, 4, QTableWidgetItem("Distance Away"))
            # Align columns to same width
            tableShortestWalk.horizontalHeader().setStretchLastSection(True)
            tableShortestWalk.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # Set columns to read only, no editing
            tableShortestWalk.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            tableLayout.addWidget(tableShortestWalk, 3, 0)

        elif self.mode == "Drive":
            lblDriveDistance = QLabel(self)
            lblDriveDistance.setText('Total Driving Distance:')
            lblDriveDistance.setFont(QFont("Arial", 14, QFont.Bold))
            lblDriveDistance.setStyleSheet('QLabel { color : Blue; }')
            tableLayout.addWidget(lblDriveDistance, 1, 0)

            lblShortestDrive = QLabel(self)
            lblShortestDrive.setText('Shortest Path by Driving:')
            lblShortestDrive.setAlignment(Qt.AlignHCenter)
            lblShortestDrive.setFont(QFont("Arial", 14, QFont.Bold))
            lblShortestDrive.setStyleSheet('QLabel { color : Red; }')
            tableLayout.addWidget(lblShortestDrive, 2, 0)

            tableShortestDrive = QTableWidget()
            tableShortestDrive.setRowCount(20)
            tableShortestDrive.setColumnCount(5)
            tableShortestDrive.setItem(0, 0, QTableWidgetItem("Starting Node"))
            tableShortestDrive.setItem(0, 1, QTableWidgetItem("Target Node"))
            tableShortestDrive.setItem(0, 2, QTableWidgetItem("Cost"))
            tableShortestDrive.setItem(0, 3, QTableWidgetItem("Estimated time taken to reach"))
            tableShortestDrive.setItem(0, 4, QTableWidgetItem("Distance Away"))
            # Align columns to same width
            tableShortestDrive.horizontalHeader().setStretchLastSection(True)
            tableShortestDrive.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # Set columns to read only, no editing
            tableShortestDrive.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            tableLayout.addWidget(tableShortestDrive, 3, 0)

        elif self.mode == "Bus":
            lblBusDistance = QLabel(self)
            lblBusDistance.setText('Total Bus Distance:')
            lblBusDistance.setFont(QFont("Arial", 14, QFont.Bold))
            lblBusDistance.setStyleSheet('QLabel { color : Blue; }')
            tableLayout.addWidget(lblBusDistance, 1, 0)

            lblShortestBus = QLabel(self)
            lblShortestBus.setText('Shortest Path by Bus:')
            lblShortestBus.setAlignment(Qt.AlignHCenter)
            lblShortestBus.setFont(QFont("Arial", 14, QFont.Bold))
            lblShortestBus.setStyleSheet('QLabel { color : Green; }')
            tableLayout.addWidget(lblShortestBus, 2, 0)

            tableShortestBus = QTableWidget()
            tableShortestBus.setRowCount(20)
            tableShortestBus.setColumnCount(5)
            tableShortestBus.setItem(0, 0, QTableWidgetItem("Starting Node"))
            tableShortestBus.setItem(0, 1, QTableWidgetItem("Target Node"))
            tableShortestBus.setItem(0, 2, QTableWidgetItem("Cost"))
            tableShortestBus.setItem(0, 3, QTableWidgetItem("Estimated time taken to reach"))
            tableShortestBus.setItem(0, 4, QTableWidgetItem("Distance Away"))
            tableShortestBus.horizontalHeader().setStretchLastSection(True)
            tableShortestBus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tableShortestBus.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            tableLayout.addWidget(tableShortestBus, 3, 0)

        else:
            lblTrainDistance = QLabel(self)
            lblTrainDistance.setText('Total Train Distance:')
            lblTrainDistance.setFont(QFont("Arial", 14, QFont.Bold))
            lblTrainDistance.setStyleSheet('QLabel { color : Blue; }')
            tableLayout.addWidget(lblTrainDistance, 1, 0)

            lblShortestTrain = QLabel(self)
            lblShortestTrain.setText('Shortest Path by Train:')
            lblShortestTrain.setAlignment(Qt.AlignHCenter)
            lblShortestTrain.setFont(QFont("Arial", 14, QFont.Bold))
            lblShortestTrain.setStyleSheet('QLabel { color : Purple; }')
            tableLayout.addWidget(lblShortestTrain, 2, 0)

            tableShortestTrain = QTableWidget()
            tableShortestTrain.setRowCount(20)
            tableShortestTrain.setColumnCount(5)
            tableShortestTrain.setItem(0, 0, QTableWidgetItem("Starting Node"))
            tableShortestTrain.setItem(0, 1, QTableWidgetItem("Target Node"))
            tableShortestTrain.setItem(0, 2, QTableWidgetItem("Cost"))
            tableShortestTrain.setItem(0, 3, QTableWidgetItem("Estimated time taken to reach"))
            tableShortestTrain.setItem(0, 4, QTableWidgetItem("Distance Away"))
            tableShortestTrain.horizontalHeader().setStretchLastSection(True)
            tableShortestTrain.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tableShortestTrain.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            tableLayout.addWidget(tableShortestTrain, 3, 0)

        gridLayout.addLayout(tableLayout, 1, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shortest = ShortestPathGUI()
    sys.exit(app.exec_())