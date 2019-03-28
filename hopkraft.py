#Algorithms for bipartite graphs

import networkx as nx
import collections

class HopcroftKarp(object):
    INFINITY = -1

    def __init__(self, G):
        self.G = G

    def match(self):
        self.N1, self.N2 = self.partition()
        self.pair = {}
        self.dist = {}
        self.q = collections.deque()

        #init
        for v in self.G:
            self.pair[v] = None
            self.dist[v] = HopcroftKarp.INFINITY

        matching = 0

        while self.bfs():
            for v in self.N1:
                if self.pair[v] is None and self.dfs(v):
                    matching = matching + 1

        return matching

    def dfs(self, v):
        if v != None:
            for u in self.G.neighbors(v):
                if self.dist[ self.pair[u] ] == self.dist[v] + 1 and self.dfs(self.pair[u]):
                    self.pair[u] = v
                    self.pair[v] = u

                    return True

            self.dist[v] = HopcroftKarp.INFINITY
            return False

        return True

    def bfs(self):
        for v in self.N1:
            if self.pair[v] is None:
                self.dist[v] = 0
                self.q.append(v)
            else:
                self.dist[v] = HopcroftKarp.INFINITY

        self.dist[None] = HopcroftKarp.INFINITY

        while len(self.q) > 0:
            v = self.q.popleft()
            if v != None:
                for u in self.G.neighbors(v):
                    if self.dist[ self.pair[u] ] == HopcroftKarp.INFINITY:
                        self.dist[ self.pair[u] ] = self.dist[v] + 1
                        self.q.append(self.pair[u])

        return self.dist[None] != HopcroftKarp.INFINITY


    def partition(self):
        return nx.algorithms.bipartite.basic.sets(self.G)

G = nx.Graph([
(1,"a"), (1,"c"),
(2,"a"), (2,"b"),
(3,"a"), (3,"c"),
(4,"d"), (4,"e"),(4,"f"),(4,"g"),
(5,"b"), (5,"c"),
(6,"c"), (6,"d")
])

matching = HopcroftKarp(G).match()

print(matching)
# print(list(G.nodes()))
# print(list(G.edges()))