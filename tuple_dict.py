# Implementing a tuple dictionary (s, s_next) -> p

tuple_dict = {}

tuple_dict['foo'] = 'bar'
tuple_dict[(2, 3)] = 'bar'

x = 2
y = 3

print(tuple_dict[(x, y)])

# Reading and converting txt to tuple dict [(x,y)] -> z

import numpy as np

array_test = np.loadtxt('Ambientes/Ambiente1/Action_Sur.txt')

array_dict = {}
for element in array_test:
    array_dict[(int(element[0]), int(element[1]))] = element[2]
    

