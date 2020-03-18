import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class DrivingPathGUI(QtWidgets.QMainWindow):
    def __init__(self, startLocation, endLocation):
        super().__init__()
        self.title = 'ICT1008 AY19/20 Project Group 2-3'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.startLocation = startLocation
        self.endLocation = endLocation
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
        tableShortestDrive.setColumnCount(3)
        tableShortestDrive.setItem(0, 0, QTableWidgetItem("Starting Node Coordinates"))
        tableShortestDrive.setItem(0, 1, QTableWidgetItem("Target Node Coordinates"))
        tableShortestDrive.setItem(0, 2, QTableWidgetItem("Cost"))

        # Align columns to same width
        tableShortestDrive.horizontalHeader().setStretchLastSection(True)
        tableShortestDrive.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set columns to read only, no editing
        tableShortestDrive.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        tableLayout.addWidget(tableShortestDrive, 3, 0)


        gridLayout.addLayout(tableLayout, 1, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shortest = ShortestPathGUI()
    sys.exit(app.exec_())