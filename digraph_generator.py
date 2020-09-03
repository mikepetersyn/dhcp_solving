import networkx as nx
from random import randint
import matplotlib.pyplot as plt


def get_complete_digraph(n):
    return nx.complete_graph(n).to_directed()


def get_grid_2d_digraph(m, n):
    return nx.grid_2d_graph(m, n).to_directed()


def get_erdos_renyi_digraph(n, p):
    return nx.erdos_renyi_graph(n, p, directed=True)


