import timeit
import numpy as np
from digraph_generator import *
from hamiltonian import *
from profiler import *


@profile
def call_hamiltonian(hamiltonian_obj: Hamiltonian):
    hamiltonian_obj.get_hamilton_cycle()


def test_problem(p, is_decision=False):
    list_runtime_all = []
    for n in range(17, 21):
        for i in range(0, 50):
            print('Round {}/49 with n={}, p={}, decision={}'.format(i, n, p, is_decision))
            G = get_erdos_renyi_digraph(n, p)
            call_hamiltonian(Hamiltonian(G, is_decision))
        prof_data = get_prof_data()
        prof_data['n'] = n
        print('Result: {} \n'.format(prof_data))
        list_runtime_all.append(prof_data)
        clear_prof_data()
    return list_runtime_all


def experiment():
    # p is the probability for edge creation: the higher the value
    # the more dense is the graph
    for p in [0.20, 0.25, 0.30, 0.35]:
        # run the decision problem experiment and save array to disk
        decision_log = test_problem(p, is_decision=True)
        #search_log = test_problem(p, is_decision=False)
        np.savez_compressed('data/decision_p_{}.npz'.format(p), a=np.array(decision_log))
        #np.savez_compressed('data/search_p_{}.npz'.format(p), a=np.array(search_log))


experiment()
