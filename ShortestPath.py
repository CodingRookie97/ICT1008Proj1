from collections import defaultdict
from haversine import haversine

global mapView

MAX_WALK_RANGE = 0.5 # km

class ShortestPath:

    def __init__(self, nodes):
        self.nodes = nodes
        self.edges = []
        self.mrtnodes = {}
        self.mrtroutes = {}

    def create_edges(self):
        for key1, value1 in self.nodes.items():
            for key2, value2 in self.nodes.items():
                edge = add_neighbour(key1, value1, key2, value2)
                if edge is not None:
                    self.edges.append(edge)

    def create_mrt_edgenodes(self, edges, mrtnodes, mrtroutes):
        self.edges = self.edges + edges
        self.mrtnodes = mrtnodes
        self.mrtroutes = mrtroutes

    def build_graph(self):
        graph = defaultdict(list)
        seen_edges = defaultdict(int)
        for src, dst, weight, mode in self.edges:
            seen_edges[(src, dst, weight)] += 1
            if seen_edges[(src, dst, weight)] > 1:
                continue
            graph[src].append([dst, weight, mode])
            # remove this line of edge list is directed
            graph[dst].append([src, weight, mode])
        return graph

    def find_shortest_path(self, graph, src, dst):
        d, prev = dijkstra(graph, src, dst)
        path = find_path(prev, [dst, 'walk'])
        newpath=[]
        for x in path:
            if x[0] in self.nodes:
                newpath.append(swap(self.nodes[x[0]]))
            elif x[0] in self.mrtnodes:
                newpath.append(swap(self.mrtnodes[x[0]]))
            elif x[1] == "LRT":
                newpath.append(swap(self.mrtroutes[x[0]]))
        return newpath

def dijkstra(graph, src, dst=None):
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
        u = min(q, key=dist.get)
        q.remove(u)

        if dst is not None and u == dst:
            return dist[dst], prev

        for v, w, mode in graph.get(u, []):

            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = [u, mode]
    return dist, prev

def add_neighbour(key1, value1, key2, value2):
    distance = haversine(value1, value2)
    if distance < MAX_WALK_RANGE:
        return [key1, key2, distance, 'walk']

def find_path(prv, node):
    p = []

    while node is not None:
        p.append(node)
        node = prv[node[0]]
    return p[::-1]

def swap(coord):
    return [coord[1], coord[0]]