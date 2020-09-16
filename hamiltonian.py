import networkx as nx
import scipy as sp
from digraph_generator import *


class Hamiltonian:

    def __init__(self, G, is_decision):
        self.G = nx.adjacency_matrix(G).todense()
        self.n = len(self.G)
        self.walk = self.init_walk()
        self.found = 0
        self.is_decision = is_decision
        self.running = True

    def init_walk(self):
        walk = [-1] * self.n
        walk[0] = 0
        return walk

    def is_adjacent(self, a, b):
        return self.G[self.walk[a], self.walk[b]] == 1

    def is_duplicate(self, k):
        for i in range(0, k):
            if self.walk[i] == self.walk[k]:
                return True
        return False

    def get_hamilton_cycle(self, k=1):
        while self.running:
            self.bounding(k)

            if self.walk[k] == -1:
                return
            elif k == self.n - 1:
                self.found += 1
                if self.is_decision:
                    self.running = False
                    return
            else:
                self.get_hamilton_cycle(k + 1)

    def bounding(self, k):
        while True:
            self.walk[k] = (self.walk[k] + 1) % (self.n+1)

            if self.walk[k] == self.n:
                self.walk[k] = -1
                return

            if self.is_adjacent(k - 1, k):

                if not self.is_duplicate(k):
                    if (k < self.n - 1) or (
                            k == self.n - 1 and
                            self.is_adjacent(k, 0)):
                        return
