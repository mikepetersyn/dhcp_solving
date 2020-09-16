from typing import Tuple
import copy
import numpy as np
import networkx as nx
import random as rd
import matplotlib.pyplot as plt
from digraph_generator import *


class DHC:

    def __init__(self, adj_mat):
        self.ADJ_MAT = adj_mat
        self.G = nx.to_networkx_graph(
            self.ADJ_MAT, create_using=nx.DiGraph)
        self.round_adj_mat = copy.deepcopy(
            self.ADJ_MAT)
        self.n = len(self.ADJ_MAT)

    def reset_round_adj_mat(self):
        self.round_adj_mat = copy.deepcopy(
            self.ADJ_MAT)

    def select(self, u):
        neighbours = np.where(
            self.round_adj_mat[u] == 1)[1]
        if len(neighbours) > 0:
            v = neighbours[rd.randint(
                0, len(neighbours) - 1)]
            self.delete_edge(u, v)
            return v
        else:
            return None

    def delete_edge(self, u, v):
        self.round_adj_mat[u, v] = 0

    def get_distance(self, path, ndp, v):
        return path.index(ndp) - path.index(v)

    def run(self):
        c = []
        path = []
        s = rd.randint(0, len(
            self.round_adj_mat) - 1)
        path.append(s)
        ndp = s
        mode = 2
        while True:
            v = self.select(ndp)
            if v is None:
                print('No Cycle found.')
                return None
            else:
                if mode == 2:
                    if v != s and v not in path:
                        path.append(v)
                        ndp = v
                    if v != s and v in path and \
                            self.get_distance(
                                path, ndp, v) >= self.n / 2:
                        u_i = path.index(v) - 1
                        u = path[u_i]
                        c = path[u_i:]
                        path = path[:u_i]
                        ndp = u
                        mode = 3
                elif mode == 3:
                    if v != s and v not in path:
                        path.append(v)
                        ndp = v
                    elif v in c:
                        path.append(c)
                        u_i = c.index(v) - 1
                        u = c[u_i]
                        path = c
                        c = []
                        ndp = u
            if len(path) == self.n and \
                    self.round_adj_mat[path[-1], s] == 1:
                path.append(s)
                print(path)
                return True

G = get_erdos_renyi_digraph(20, 0.3)
a = nx.adjacency_matrix(G).todense()
dhc = DHC(a)

for i in range(0, 100000):
    dhc.run()
