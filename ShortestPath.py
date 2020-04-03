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
    def create_edges(self):
        for key1, value1 in self.nodes.items():
            for key2, value2 in self.nodes.items():
                #add a new neighbouring node
                edge = add_neighbouring_nodes(key1, value1, key2, value2)
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
    def build_graph(self):
        graph = defaultdict(list)
        visited_edges = defaultdict(int)
        for src, dst, weight, mode in self.edges:
            #flag to check if the same edge has been visited or not
            visited_edges[(src, dst, weight)] += 1
            #ignore the edge to add into the graph if it is visited, else would form a cycle which is NOT a path anymore
            if visited_edges[(src, dst, weight)] > 1:
                continue
            graph[src].append([dst, weight, mode])
            graph[dst].append([src, weight, mode])
        return graph

    #Finding the shortest path via Dijkstra
    def find_shortest_path(self, graph, src, dst):
        d, prev = dijkstra(graph, src, dst)
        path = find_next_path(prev, [dst, 'walk'])
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
def dijkstra(graph, src, dst = None):
    nodes = []
    for n in graph:
        nodes.append(n)
        nodes += [x[0] for x in graph[n]]
    q = set(nodes)
    nodes = list(q)

    distance = dict()
    prev = dict()
    for n in nodes:
        #at first initialise to infinite
        distance[n] = float('inf')
        prev[n] = None

    distance[src] = 0

    while q:
        #Mark the current node as visited and remove it from the unvisited set.
        u = min(q, key=distance.get)
        q.remove(u)

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
def add_neighbouring_nodes(key1, value1, key2, value2):
    distance = haversine(value1, value2)
    #specify the range of which the distance is within the walking range of 0.5 from a coordinate checkpoint
    if distance < 0.5:
        return [key1, key2, distance, 'walk']

#Find path to connect from previous node
def find_next_path(prv, node):
    path = []

    while node is not None:
        path.append(node)
        node = prv[node[0]]
    return path[::-1]

#Swap long and lat to support lat first then long
def swapCoordinates(coord):
    return [coord[1], coord[0]]