import folium
import os

nodeMap = folium.Map(location=[1.4053, 103.9021], zoom_start=16)
nodes = os.path.join('nodes.json')
folium.GeoJson(nodes).add_to(nodeMap)

nodeMap.save('C:\\Users\\Jerone Poh\\Desktop\\punggol.html')