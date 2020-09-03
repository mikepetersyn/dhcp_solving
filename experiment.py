import timeit
import numpy as np
from digraph_generator import *
from hamiltonian import *


def get_runtime_format(n, p, start, stop):
    return 'Nodes: {}, Probability: {}, Runtime: {}'.format(n, p, (stop - start))


def test_decision_problem(p):
    list_runtime_all = []
    for n in range(5, 25):
        list_runtime = []
        for i in range(0, 50):
            print('Round {}/49 with n={}, p={}'.format(i, n, p))
            G = get_erdos_renyi_digraph(n, p)
            start = timeit.default_timer()
            hamiltonian = Hamiltonian(G, True)
            stop = timeit.default_timer()
            hamiltonian.get_hamilton_cycle()
            list_runtime.append(get_runtime_format(n, p, start, stop))
        list_runtime_all.append(list_runtime)
    return list_runtime_all


def test_search_problem(p):
    list_runtime_all = []
    for n in range(5, 25):
        list_runtime = []
        for i in range(0, 50):
            print('Round {}/49 with n={}, p={}'.format(i, n, p))
            G = get_erdos_renyi_digraph(n, p)
            start = timeit.default_timer()
            hamiltonian = Hamiltonian(G, False)
            stop = timeit.default_timer()
            hamiltonian.get_hamilton_cycle()
            list_runtime.append(get_runtime_format(n, p, start, stop))
        list_runtime_all.append(list_runtime)
    return list_runtime_all

def experiment():
    # p is the probability for edge creation: the higher the value
    # the more dense is the graph
    for p in [0.15, 0.20, 0.25, 0.30, 0.35, 0.45, 0.50]:
        # run the decision problem experiment and save array to disk
        runtime_decision = test_decision_problem(p)
        np.savez_compressed('data/decision_problem_experiment_array_p-{}.npz'.format(p), a=np.array(runtime_decision))


experiment()


