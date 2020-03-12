import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class FastestPathGUI(QtWidgets.QMainWindow):
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

        lblFastestPathTitle = QLabel(self)
        lblFastestPathTitle.setText('Compute Fastest Path')
        lblFastestPathTitle.setAlignment(Qt.AlignHCenter)
        lblFastestPathTitle.setFont(QFont("Arial", 20, QFont.Bold))
        lblFastestPathTitle.setStyleSheet('QLabel { color : Green; }')
        lblFastestPathTitle.adjustSize()
        titleLayout.addWidget(lblFastestPathTitle)

        gridLayout.addLayout(titleLayout, 0, 0)
        tableLayout = QtWidgets.QGridLayout(self.main)

        lblBusDistance = QLabel(self)
        lblBusDistance.setText('Total Bus Distance:')
        lblBusDistance.setFont(QFont("Arial", 14, QFont.Bold))
        lblBusDistance.setStyleSheet('QLabel { color : Blue; }')
        tableLayout.addWidget(lblBusDistance, 1, 0)

        lblFastestBus = QLabel(self)
        lblFastestBus.setText('Fastest Path by Bus:')
        lblFastestBus.setAlignment(Qt.AlignHCenter)
        lblFastestBus.setFont(QFont("Arial", 14, QFont.Bold))
        lblFastestBus.setStyleSheet('QLabel { color : Green; }')
        tableLayout.addWidget(lblFastestBus, 2, 0)

        tableFastestBus = QTableWidget()
        tableFastestBus.setRowCount(20)
        tableFastestBus.setColumnCount(5)
        tableFastestBus.setItem(0, 0, QTableWidgetItem("Starting Node"))
        tableFastestBus.setItem(0, 1, QTableWidgetItem("Target Node"))
        tableFastestBus.setItem(0, 2, QTableWidgetItem("Cost"))
        tableFastestBus.setItem(0, 3, QTableWidgetItem("Estimated time taken to reach"))
        tableFastestBus.setItem(0, 4, QTableWidgetItem("Distance Away"))
        tableFastestBus.horizontalHeader().setStretchLastSection(True)
        tableFastestBus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableFastestBus.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        tableLayout.addWidget(tableFastestBus, 3, 0)

        lblTrainDistance = QLabel(self)
        lblTrainDistance.setText('Total Train Distance:')
        lblTrainDistance.setFont(QFont("Arial", 14, QFont.Bold))
        lblTrainDistance.setStyleSheet('QLabel { color : Blue; }')
        tableLayout.addWidget(lblTrainDistance, 4, 0)

        lblFastestTrain = QLabel(self)
        lblFastestTrain.setText('Fastest Path by Train:')
        lblFastestTrain.setAlignment(Qt.AlignHCenter)
        lblFastestTrain.setFont(QFont("Arial", 14, QFont.Bold))
        lblFastestTrain.setStyleSheet('QLabel { color : Purple; }')
        tableLayout.addWidget(lblFastestTrain, 5, 0)

        tableFastestTrain = QTableWidget()
        tableFastestTrain.setRowCount(20)
        tableFastestTrain.setColumnCount(5)
        tableFastestTrain.setItem(0, 0, QTableWidgetItem("Starting Node"))
        tableFastestTrain.setItem(0, 1, QTableWidgetItem("Target Node"))
        tableFastestTrain.setItem(0, 2, QTableWidgetItem("Cost"))
        tableFastestTrain.setItem(0, 3, QTableWidgetItem("Estimated time taken to reach"))
        tableFastestTrain.setItem(0, 4, QTableWidgetItem("Distance Away"))
        tableFastestTrain.horizontalHeader().setStretchLastSection(True)
        tableFastestTrain.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableFastestTrain.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        tableLayout.addWidget(tableFastestTrain, 6, 0)

        gridLayout.addLayout(tableLayout, 1, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shortest = FastestPathGUI()
    sys.exit(app.exec_())