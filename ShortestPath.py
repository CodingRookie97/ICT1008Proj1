from collections import defaultdict
from haversine import haversine

global mapView

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
                edge = add_neighbour(key1, value1, key2, value2)
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
        path = find_path(prev, [dst, 'walk'])
        shortestPath = []
        for x in path:
            if x[0] in self.nodes:
                #swap coordinates of the nodes during program runtime
                shortestPath.append(swap(self.nodes[x[0]]))
            elif x[0] in self.mrtNodes:
                shortestPath.append(swap(self.mrtNodes[x[0]]))
            elif x[0] in self.busNodes:
                shortestPath.append(swap(self.busNodes[x[0]]))

            #if mode is Bus
            elif x[1] == "Bus":
                shortestPath.append(swap(self.busRoutes[x[0]]))

            #if mode is LRT
            elif x[1] == "LRT":
                shortestPath.append(swap(self.mrtRoutes[x[0]]))
        return shortestPath

#Dijkstra algorithm to find shorest distance away from a coordinate
#Source adapted from: https://dev.to/mxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc
def dijkstra(graph, src, dst = None):
    nodes = []
    for n in graph:
        nodes.append(n)
        nodes += [x[0] for x in graph[n]]
    q = set(nodes)
    nodes = list(q)

    dist = dict()
    prev = dict()
    for n in nodes:
        dist[n] = float('inf')
        prev[n] = None

    dist[src] = 0

    while q:
        #Mark the current node as visited and remove it from the unvisited set.
        u = min(q, key=dist.get)
        q.remove(u)

        if dst is not None and u == dst:
            return dist[dst], prev

        for v, w, mode in graph.get(u, []):

            # Compare the newly calculated distance to the assigned and save the smaller one.
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = [u, mode]
    return dist, prev

#This is to add a neighbouring node to determine which coordinate is the nearest from the checkpoint via walking
def add_neighbour(key1, value1, key2, value2):
    distance = haversine(value1, value2)
    #specify the range of which the distance is within the walking range of 0.5 from a coordinate checkpoint
    if distance < 0.5:
        return [key1, key2, distance, 'walk']

#Find path to connect from previous node
def find_path(prv, node):
    p = []

    while node is not None:
        p.append(node)
        node = prv[node[0]]
    return p[::-1]

#Swap long and lat to support lat first then long
def swap(coord):
    return [coord[1], coord[0]]