<h4>ICT1008 AY2019/20 Data Structures & Algorithms Project</h4>
<h4>Group P2-3</h4>
<p><b>Project Title: It's all about Punggol West!</b></p>
<p><i>Developing a program to route the shortest path from a
selected start point to a selected end point using different
modes of transportation. This program only covers a selected
area of Punggol West.</i></p>
<h4>JSON FILE Dataset</h4>
<p>This program uses data stored in .json files for the
majority of its operations.</p>
<p>JSON files used for this program:</p>
<p><b>Location Data:</b></p>
<p><i>Coordinates for HDB blocks and major landmarks in the area
of interest. <br> Stored within the Buildings folder.</i></p>
<ol>
<li>General Landmarks Dataset: general_buildings.json</li>
<li>HDB Landmarks Dataset: residential_buildings.json</li>
</ol>
<p><b>MRT Data:</b></p>
<p><i>Coordinates for all MRT stations and data on train paths.
<br> Stored within the MRT folder.</i></p>
<ol>
<li>MRT/LRT Stations Dataset: mrt.json</li>
<li>Entire Punggol West LRT Line Path Dataset: train.geojson</li>
</ol>
<p><b>Bus Data:</b></p>
<p><i>Coordinates for all bus stops and data on bus services
and the bus routes taken by each of these services.
Also contains additional road coordinates to help the program plot
better paths in a visual format.
<br> Stored in Bus_Stops, Bus_Services and Bus_Path respectively.</i></p>
<ol>
<li>Bus Stops Dataset: bus_stop.json</li>
<li>Bus Services Dataset: Bus_XX_from.json</li>
<li>Road Dataset</li>
</ol>
<p><b>Combined Data:</b></p>
<p><i>A combined data set with major information from each to make accessing
data easier for the program.
<br> Stored within the Combined folder.</i></p>
<ol>
<li>Combined Landmarks + MRT + Bus Datasets: nodes.json</li>
</ol>
<h4>Prerequisite Downloads</h4>
<p>In order to run the application successfully, you are strongly
encouraged to download and install the packages listed below:</p>
<p><b>1. Python 3.x: Python version 3.x or up is required.
</b></p>
<p>Latest version is recommended.
<br>Download from: <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a><br>
</p>
<p><b>2. PyQt5: Python's GUI framework</b></p>
<p>Run this command through the command line:
<br><i>pip install PyQt5</i></p>
<p><b>3. PyQtWebEngine: A set of Python bindings for The Qt Company’s
Qt WebEngine framework.</b></p>
<p>Run this command through the command line:
<br><i>pip install PyQtWebEngine</i></p>
<p><b>4. Folium: Parsed Open Street Map API to display the Leaflet map in Python.
</b></p>
<p>Run this command through the command line:
<br><i>pip install folium</i></p>
<p><b>5. Haversine: Dynamically calculates the distance (in km) between 2 coordinates that can be used for Dijkstra Algorithm.
</b></p>
<p>Run this command through the command line:
<br><i>pip install haversine</i></p>
<h4>Main Functions</h4>
<p>The main functions of this program:</p>
<li>Displaying 4 different kinds of nodes into the folium map that is represented by different logos for different landmarks</li>
<li>Allowing users to select any starting and ending location to determine the shortest path to reach their destination</li>
<li>Displaying bus routes for the bus services that ply through Punggol West</li>
<li>Displaying the shortest walking path, fastest bus path, fastest train path via different colours in the map</li>
<h4>Algorithm Used</h4>
<p>This program uses Dijkstra's algorithm to determine:</p>
<ol>
<li>Shortest Walking Path</li>
<li>Fastest Bus Path</li>
<li>Fastest Train Path</li>
</ol>
<h4>Data Structures Used</h4>
<p>This program uses these data structures:</p>
<ol><li>Ordered Dictionary: To store node information for the paths.</li>
<li>List: To store relevant node information from our datasets.</li></ol>
<h4>References</h4>
<p>These are the websites that we have referenced from during our research & development phase:</p>
<ol><li><b>Folium (Python parser to parse map from HTML to Python): </b><a href="https://python-visualization.github.io/folium/">https://python-visualization.github.io/folium/</a></li>
<li><b>GeoJSON (Manual plotting of the nodes, area of interest outline, bus service routes): </b><a href="http://geojson.io/">http://geojson.io/</a></li>
<li><b>PyQt5 (For GUI purposes): </b><a href="https://pypi.org/project/PyQt5">https://pypi.org/project/PyQt5/</a></li>
<li><b>Overpass Turbo EU (To query the results to retrieve selected coordinates from Open Street Map: </b><a href="https://overpass-turbo.eu/">https://overpass-turbo.eu/</a></li>
<li><b>Bus Router SG (Plotting out the bus routes and deciding on bus stop coordinates): </b><a href="https://busrouter.sg/">https://busrouter.sg/</a></li>
<li><b>Dijkstra Algorithm: </b><a href="https://dev.to/mxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc">https://dev.to/mxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc</a></li>
<li><b>How to include Folium map into PyQt5 Window: </b><a href="https://stackoverflow.com/questions/60437182/how-to-include-folium-map-into-pyqt5-application-window">https://stackoverflow.com/questions/60437182/how-to-include-folium-map-into-pyqt5-application-window</a></li>
</ol>