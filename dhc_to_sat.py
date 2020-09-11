import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class DHCtoSAT:

    def __init__(self, adjacency_list, directed=False, dimacs=False):
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
        return {x: i + 1 for i, x in enumerate(literal_list)}

    def plot(self):
        nx.draw(self.G, with_labels=True, font_weight='bold')
        plt.show()

    def no_close_loop(self):
        for x in self.literals:
            for y in self.literals:
                if x[0] == y[1] and x[1] == y[0]:
                    if self.dimacs_dict is not None:
                        print('-{} -{} 0'.format(self.dimacs_dict[x], self.dimacs_dict[y]))
                    else:
                        print('-{} V -{}'.format(x, y))

    def no_duplicate_head(self):
        for x in self.literals:
            for y in self.literals:
                if x[0] == y[0] and x[1] != y[1]:
                    if self.dimacs_dict is not None:
                        print('-{} -{} 0'.format(self.dimacs_dict[x], self.dimacs_dict[y]))
                    else:
                        print('-{} V -{}'.format(x, y))

    def no_duplicate_tail(self):
        for x in self.literals:
            for y in self.literals:
                if x[0] != y[0] and x[1] == y[1]:
                    if self.dimacs_dict is not None:
                        print('-{} -{} 0'.format(self.dimacs_dict[x], self.dimacs_dict[y]))
                    else:
                        print('-{} V -{}'.format(x, y))

    def one_outgoing_edge(self):
        for i, x in enumerate(self.literals):
            curr = []
            for y in self.literals:
                if i == y[0]:
                    curr.append(y)
            if len(curr) == 1:
                if self.dimacs_dict is not None:
                    print('{} 0'.format(self.dimacs_dict[curr[0]]))
                else:
                    print(curr[0])
            else:
                for j, z in enumerate(curr):
                    if j < len(curr) - 1:
                        if self.dimacs_dict is not None:
                            print('{}'.format(self.dimacs_dict[z]), end=' ')
                        else:
                            print('{} V'.format(z), end=' ')
                    else:
                        if self.dimacs_dict is not None:
                            print('{} 0'.format(self.dimacs_dict[z]))
                        else:
                            print('{}'.format(z))

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
    [0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 0, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0]
])

dhc_to_sat = DHCtoSAT(b, directed=False, dimacs=True)

print(dhc_to_sat.literals)

dhc_to_sat.convert()


