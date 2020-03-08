import folium
import os
import io
import sys
import csv
from PyQt5 import QtWidgets, QtWebEngineWidgets

# Create the bus coordinates and add the line
bus3CString = ["Bus Stop 65009: Punggol Temp Interchange", "Intersection H", "Bus Stop 65221: Blk 303D"]
bus84CString = ["Bus Stop 65009: Punggol Temp Interchange", "Intersection H", "Bus Stop 65221: Blk 303D", "Intersection G", "Bus Stop 65091: Blk 301A", "Intersection F", "Intersection E", "Bus Stop 65489: Aft Punggol Drive", "Intersection Q", "Intersection D", "Intersection C", "Bus Stop 65469: Blk 310B", "Intersection B", "Bus Stop 65619: Nibong Stn Exit A"]
busCoordinatesString = []
busLat = []
busLon = []
bus3Coordinates = [[0 for x in range(2)] for y in range(3)]
bus84Coordinates = [[0 for x in range(2)] for y in range(14)]

with open('Punggol_Nodes.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        busCoordinatesString.append(row[3])
        busLat.append(row[4])
        busLon.append(row[5])

index = 0
for j in range(0, len(busCoordinatesString)):
    if bus3CString[index] in busCoordinatesString:
        bus3Coordinates[index][0] = float(busLon[busCoordinatesString.index(bus3CString[index])])
        bus3Coordinates[index][1] = float(busLat[busCoordinatesString.index(bus3CString[index])])
        index += 1
    if index == 3:
        break

index = 0
for k in range(0, len(busCoordinatesString)):
    if bus84CString[index] in busCoordinatesString:
        bus84Coordinates[index][0] = float(busLon[busCoordinatesString.index(bus84CString[index])])
        bus84Coordinates[index][1] = float(busLat[busCoordinatesString.index(bus84CString[index])])
        index += 1
    if index == 14:
        break

print(bus84CString)
print(bus84Coordinates)
app = QtWidgets.QApplication(sys.argv)
nodeMap = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
nodes = os.path.join('mrt.json')
print(bus84Coordinates)
folium.PolyLine(bus3Coordinates, color="red", weight=5).add_to(nodeMap)
folium.PolyLine(bus84Coordinates, color="blue", weight=5).add_to(nodeMap)
folium.GeoJson(nodes).add_to(nodeMap)
data = io.BytesIO()
nodeMap.save(data, close_file=False)

w = QtWebEngineWidgets.QWebEngineView()
w.setHtml(data.getvalue().decode())
w.resize(640, 480)
w.show()
sys.exit(app.exec_())
