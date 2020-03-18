import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class ShortestPathGUI(QtWidgets.QMainWindow):
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
        tableShortestWalk.setColumnCount(3)
        tableShortestWalk.setItem(0, 0, QTableWidgetItem("Starting Node Coordinates"))
        tableShortestWalk.setItem(0, 1, QTableWidgetItem("Target Node Coordinates"))
        tableShortestWalk.setItem(0, 2, QTableWidgetItem("Cost"))
        # Align columns to same width
        tableShortestWalk.horizontalHeader().setStretchLastSection(True)
        tableShortestWalk.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set columns to read only, no editing
        tableShortestWalk.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        tableLayout.addWidget(tableShortestWalk, 3, 0)

        gridLayout.addLayout(tableLayout, 1, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shortest = ShortestPathGUI()
    sys.exit(app.exec_())