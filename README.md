<h4>ICT1008 AY2019/20 Data Structures & Algorithms Project</h4>
<i>Project Title: It's all about Punggol West!</i>
<h4>Group P2-3</h4>
<h4>JSON FILE Dataset</h4>
<ol>
<li>General Landmarks Dataset: general_buildings.json</li>
<li>HDB Landmarks Dataset: residential_buildings.json</li>
</ol>
<h4>Train: Placed under MRT directory</h4>
<ol>
<li>MRT/LRT Stations Dataset: mrt.json</li>
<li>Entire Punggol West LRT Line Path Dataset: train.geojson</li>
</ol>
<h4>Bus: Placed under Bus_Stop directory for bus stops, Bus_Services for bus services and Bus_Path for road + all bus coordinates</h4>
<ol>
<li>Bus Stops Dataset: bus_stop.json</li>
<li>Bus Services Dataset: Bus_XX_from.json</li>
<li>Road Dataset</li>
</ol>
<h4>Combined: Placed under Combined directory</h4>
<ol>
<li>Combined Landmarks + MRT + Bus Datasets: nodes.json</li>
</ol>
<i>*Take note that these datasets only covers the area of Punggol West</i>
<h4>Download Instructions</h4>
These are the pre-requisities to run the application successfully, you are strongly encouraged to download the repositories as displayed below<br>
1. Python 3.x: You must have at least a Python version 3 and above, preferably in latest Python version.<br>
2. PyQt5: Python's GUI framework<br>- pip install PyQt5<br>
3. PyQtWebEngine: A set of Python bindings for The Qt Company’s Qt WebEngine framework<br>- pip install PyQtWebEngine<br>
4. Folium: Parsed Open Street Map API to display the Leaflet map in Python<br>- pip install folium<br>
5. Haversine: Dynamically calculates the distance between 2 coordinates that can be used for Dijkstra Algorithm<br>- pip install haversine
<h4>Main Functions</h4>
<li>Display of 4 different kinds of nodes into the folium map that is represented by different logos for different landmarks</li>
<li>Allowing users the freedom to select any starting and ending location to determine their shortest path to reach to their destination</li>
<li>Showing of bus routes for the bus services that ply through Punggol West</li>
<li>Displaying the shortest walking path, fastest bus path, fastest train path via different colours in the map</li>
<h4>Algorithm used</h4>
Dijkstra to find:
<ol>
<li>Shortest Walking Path</li>
<li>Fastest Bus Path</li>
<li>Fastest Train Path</li>
</ol>
<h4>Data Structures</h4>
<ol><li>Ordered Dictionary</li>
<li>List</li></ol>