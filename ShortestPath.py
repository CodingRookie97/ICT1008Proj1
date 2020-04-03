from collections import defaultdict
from haversine import haversine

global mapView

#This is the class that will determine the shortest/fastest path algorithm for the different modes of transports
class ShortestPath:

    #Initialises edges, nodes, routes
    def __init__(self, nodes):
        self.nodes = nodes
        self.edges = []
        self.busNodes = {}
        self.busRoutes = {}
        self.mrtNodes = {}
        self.mrtRoutes = {}

    #Create edges for walking path that is applicable to ALL forms of transport
    def createEdges(self):
        for k1, v1 in self.nodes.items():
            for k2, v2 in self.nodes.items():
                #add a new neighbouring node
                edge = addNeighBourNodes(k1, v1, k2, v2)
                if edge is not None:
                    self.edges.append(edge)

    #Initialise both edges and nodes that belong to buses
    def createBusEdgeNodes(self, edges, busNodes, busRoutes):
        self.edges = self.edges + edges
        self.busNodes = busNodes
        self.busRoutes = busRoutes

    #Initialise both edges and nodes that belong to MRT/train
    def createMrtEdgeNodes(self, edges, mrtNodes, mrtRoutes):
        self.edges = self.edges + edges
        self.mrtNodes = mrtNodes
        self.mrtRoutes = mrtRoutes

    #This is to gradually build up the graph to check if the edge is being visited, based on what we learned in dijkstra algorithm from Lectures to track down visited nodes
    def buildAGraph(self):
        formAGraph = defaultdict(list)
        visitedEdgesCount = defaultdict(int)
        for start, destination, distanceOfEdge, modeOfTransport in self.edges:
            #flag to check if the same edge has been visited or not
            visitedEdgesCount[(start, destination, distanceOfEdge)] += 1
            #ignore the edge to add into the graph if it is visited, else would form a cycle which is NOT a path anymore
            if visitedEdgesCount[(start, destination, distanceOfEdge)] > 1:
                continue
            formAGraph[start].append([destination, distanceOfEdge, modeOfTransport])
            formAGraph[destination].append([start, distanceOfEdge, modeOfTransport])
        return formAGraph

    #Finding the shortest path via Dijkstra
    def findShortestPath(self, graph, start, destination):
        distance, previous = dijkstra(graph, start, destination)
        path = findNextPath(previous, [destination, 'walk'])
        shortestPath = []
        for x in path:
            if x[0] in self.nodes:
                #swap coordinates of the nodes during program runtime
                shortestPath.append(swapCoordinates(self.nodes[x[0]]))
            elif x[0] in self.mrtNodes:
                shortestPath.append(swapCoordinates(self.mrtNodes[x[0]]))
            elif x[0] in self.busNodes:
                shortestPath.append(swapCoordinates(self.busNodes[x[0]]))
            #if mode is Bus
            elif x[1] == "Bus":
                shortestPath.append(swapCoordinates(self.busRoutes[x[0]]))
            #if mode is LRT
            elif x[1] == "LRT":
                shortestPath.append(swapCoordinates(self.mrtRoutes[x[0]]))
        return shortestPath

#Dijkstra algorithm to find shorest distance away from a coordinate
#Source adapted from:
#https://dev.to/mxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc
#https://startupnextdoor.com/dijkstras-algorithm-in-python-3/
def dijkstra(graph, start, dst = None):
    nodes = []
    for n in graph:
        nodes.append(n)
        nodes += [x[0] for x in graph[n]]
    markAsVisited = set(nodes)
    nodes = list(markAsVisited)

    distance = dict()
    prev = dict()
    for n in nodes:
        #at first initialise to infinite
        distance[n] = float('inf')
        prev[n] = None

    distance[start] = 0

    while markAsVisited:
        #Mark the current node as visited and remove it from the unvisited set.
        u = min(markAsVisited, key=distance.get)
        markAsVisited.remove(u)

        if dst is not None and u == dst:
            return distance[dst], prev

        for v, w, mode in graph.get(u, []):

            #Compare the newly calculated distance to the assigned and save the smaller one
            alt = distance[u] + w
            if alt < distance[v]:
                distance[v] = alt
                prev[v] = [u, mode]
    return distance, prev

#This is to add a neighbouring node to determine which coordinate is the nearest from the checkpoint via walking
def addNeighBourNodes(key1, value1, key2, value2):
    distance = haversine(value1, value2)
    #specify the range of which the distance is within the walking range of 0.5 from a coordinate checkpoint
    if distance < 0.5:
        return [key1, key2, distance, 'walk']

#Find path to connect from previous node
def findNextPath(previous, node):
    findingTheNextPath = []

    while node is not None:
        findingTheNextPath.append(node)
        node = previous[node[0]]
    return findingTheNextPath[::-1]

#Swap long and lat to support lat first then long
def swapCoordinates(coordinates):
    return [coordinates[1], coordinates[0]]