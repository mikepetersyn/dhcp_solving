import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sat_to_3sat import *


class DHCtoSAT:

    def __init__(self, adjacency_list, directed=False, dimacs=False):

        self.formula = []

        if directed:
            self.graph_type = nx.DiGraph
        else:
            self.graph_type = nx.Graph

        self.G = nx.to_networkx_graph(adjacency_list, create_using=self.graph_type)

        self.literals = self.get_literals(adjacency_list)

        if dimacs:
            self.dimacs_dict = self.get_dimacs_dict(self.literals)
        else:
            self.dimacs_dict = None

    @staticmethod
    def get_literals(adj_list):
        return [(idx[0] + 1, idx[1] + 1) for idx, x in np.ndenumerate(adj_list) if x == 1]

    @staticmethod
    def get_dimacs_dict(literal_list):
        a = {x: i + 1 for i, x in enumerate(literal_list)}
        b = {(x[0] * -1, x[1] * -1): (i + 1) * -1 for i, x in enumerate(literal_list)}
        a.update(b)
        return a

    def add_to_formula(self, clause):
        self.formula.append(clause)

    @staticmethod
    def print_formula(G, formula, dimacs_dict=None):
        if dimacs_dict is not None:
            print('p cnf {} {}'.format(len(G.nodes()), len(formula)))
        for clause in formula:
            for i, literal in enumerate(clause):
                if i < len(clause) - 1:
                    if dimacs_dict is not None:
                        print('{}'.format(literal), end=' ')
                    else:
                        print('{} V'.format(literal), end=' ')
                else:
                    if dimacs_dict is not None:
                        print('{} 0'.format(literal))
                    else:
                        print('{}'.format(literal))

    def plot(self):
        nx.draw(self.G, with_labels=True, font_weight='bold')
        plt.show()

    def no_close_loop(self):
        for x in self.literals:
            for y in self.literals:
                if x[0] == y[1] and x[1] == y[0]:
                    if self.dimacs_dict is not None:
                        self.add_to_formula(
                            [self.dimacs_dict[(x[0] * -1, x[1] * -1)], self.dimacs_dict[(y[0] * -1, y[1] * -1)]])
                    else:
                        self.add_to_formula([(x[0] * -1, x[1] * -1), (y[0] * -1, y[1] * -1)])

    def no_duplicate_head(self):
        for x in self.literals:
            for y in self.literals:
                if x[0] == y[0] and x[1] != y[1]:
                    if self.dimacs_dict is not None:
                        self.add_to_formula(
                            [self.dimacs_dict[(x[0] * -1, x[1] * -1)], self.dimacs_dict[(y[0] * -1, y[1] * -1)]])
                    else:
                        self.add_to_formula([(x[0] * -1, x[1] * -1), (y[0] * -1, y[1] * -1)])

    def no_duplicate_tail(self):
        for x in self.literals:
            for y in self.literals:
                if x[0] != y[0] and x[1] == y[1]:
                    if self.dimacs_dict is not None:
                        self.add_to_formula(
                            [self.dimacs_dict[(x[0] * -1, x[1] * -1)], self.dimacs_dict[(y[0] * -1, y[1] * -1)]])
                    else:
                        self.add_to_formula([(x[0] * -1, x[1] * -1), (y[0] * -1, y[1] * -1)])

    def one_outgoing_edge(self):
        for i, x in enumerate(self.literals):
            curr = []
            for y in self.literals:
                if i == y[0]:
                    curr.append(y)
            if len(curr) == 1:
                if self.dimacs_dict is not None:
                    self.add_to_formula([self.dimacs_dict[curr[0]]])
                else:
                    self.add_to_formula(curr)
            else:
                if len(curr) != 0:
                    if self.dimacs_dict is not None:
                        for j, literal in enumerate(curr):
                            curr[j] = self.dimacs_dict[literal]
                    self.add_to_formula(curr)

    def convert(self):
        self.no_close_loop()
        self.no_duplicate_head()
        self.no_duplicate_tail()
        self.one_outgoing_edge()


a = np.array([
    [0, 1, 0, 0],
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [0, 0, 1, 0]
])

b = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
])

c = np.array([
    [0, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 1],
    [0, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 1]
])

dhc_to_sat = DHCtoSAT(a, directed=True, dimacs=True)
dhc_to_sat.convert()
dhc_to_sat.print_formula(dhc_to_sat.G, dhc_to_sat.formula, dhc_to_sat.dimacs_dict)
print('--------------------')

sat_to_3sat = SATto3SAT(dhc_to_sat.formula, dhc_to_sat.dimacs_dict)
t_sat = sat_to_3sat.convert()
dhc_to_sat.print_formula(dhc_to_sat.G, t_sat, sat_to_3sat.dimacs_dict)
