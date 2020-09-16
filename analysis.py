import numpy as np
import timeit
import time


data_path = 'data/exact'

for i in [0.2, 0.25,  0.3, 0.35]:
    a = np.load('{}/search_p_{}.npz'.format(data_path, i), allow_pickle=True)['a']
    print('{}\n'.format(i))
    for entry in a:
        print('({},{})'.format(round(entry['n'], 7), round(entry['max_time'], 7)), end='')
    print('\n')

