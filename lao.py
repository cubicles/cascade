import numpy as np
import random

def init_mdp(ambiente: int, delta_value: float):
    ''' Inicializa mdp: estados, recompensas, transicion, heuristicas
        type: "5x25", "20x100", "50x250"
    '''
    # actions: 4 acciones: norte, sur, este, oeste
    # states: Revisa 'ambiente' y lista estados
    # rewards: Revisar el archivo de costos
    # heuristics: LAO
    # transition: Funcion aparte
    # initial state: Revisa 'ambiente' y lista 0s

    # actions
    actions = (1, 2, 3, 4) # 1: este, 2: oeste, 3: norte, 4: sur

    # states
    if ambiente == 1:
        states = tuple(np.arange(1, 5*25 + 1))
    elif ambiente == 2:
        states = tuple(np.arange(1, 20*100 + 1))
    elif ambiente == 3:
        states = tuple(np.arange(1, 50*250 + 1))
    else:
        states = 0
        print("Error en la asignacion de estados")

    # rewards
    if ambiente == 1:
        cost = [1.0] * 5*25
        cost[101] = 0.0
    elif ambiente == 2:
        cost = [1.0] * 20*100
        cost[1901] = 0.0
    elif ambiente == 3:
        cost = [1.0] * 50*250
        cost[12251] = 0.0
    else:
        cost = 0
        print("Error en la asignacion de costos")

    # estado inicial
    if ambiente == 1:
        V = [0.0] * 5*25
    elif ambiente == 2:
        V = [0.0] * 20*100
    elif ambiente == 3:
        V = [0.0] * 50*250
    else:
        V = 0
        print("Error en los valores iniciales")

    # gamma / factor de descuento
    gamma = 1

    # delta
    delta = delta_value

    #heuristic
    if ambiente == 1:
        heuristic = [0.0] * 5*25
    elif ambiente == 2:
        heuristic = [0.0] * 20*100
    elif ambiente == 3:
         heuristic = [0.0] * 50*250
    else:
        heuristic = 0
        print("Error en las heuristicas iniciales")

   

    return actions, states, cost, gamma, V, delta, heuristic

def init_ftran(ambiente: int):
    PATH = f'Ambientes/Ambiente{ambiente}'
    array_norte = np.loadtxt(f'{PATH}/Action_Norte.txt')
    array_sur = np.loadtxt(f'{PATH}/Action_Sur.txt')
    array_este = np.loadtxt(f'{PATH}/Action_Este.txt')
    array_oeste = np.loadtxt(f'{PATH}/Action_Oeste.txt')

    dict_norte = {}
    dict_sur = {}
    dict_este = {}
    dict_oeste = {}

    for element in array_norte:
        dict_norte[(int(element[0]), int(element[1]))] = element[2]
    for element in array_sur:
        dict_sur[(int(element[0]), int(element[1]))] = element[2]
    for element in array_este:
        dict_este[(int(element[0]), int(element[1]))] = element[2]
    for element in array_oeste:
        dict_oeste[(int(element[0]), int(element[1]))] = element[2]

    return dict_norte, dict_sur, dict_este, dict_oeste

def ftran(s: int, s_next: int, a: int, dict_norte, dict_sur, dict_este, dict_oeste):
    ''' ftran
        Recibe s, s', a (estado inicial, final y accion) y los dataframes
    '''
    # 1: este, 2: oeste, 3: norte, 4: sur
    if a == 1:
        try:
            return dict_este[(s, s_next)]
        except:
            return 0
    elif a == 2:
        try:
            return dict_oeste[(s, s_next)]
        except:
            return 0
    elif a == 3:
        try:
            return dict_norte[(s, s_next)]
        except:
            return 0
    elif a == 4:
        try:
            return dict_sur[(s, s_next)]
        except:
            return 0
    else:
        return 0

def algo_vi(actions, states, cost, gamma, V, delta, dict_norte, dict_sur, dict_este, dict_oeste):
    ''' algo_vi
        Recibe acciones, estados, costo, gamma y valores V, corre el algo
        value iteration y devuelve la lista de valores para los estados
    '''
    max_diff_value = 0
    max_iter = 10000
    for i in range (100):
        max_diff = 0.0
        V_new = V.copy()
        for s in states:
            min_value = 100.0
            for a in actions:
                val = cost[s-1]
                for s_next in states:
                    val += ftran(s, s_next, a,
                           dict_norte, dict_sur, dict_este, dict_oeste)\
                           * (0.9 * V[s_next-1])

                # Min value
                min_value = min(min_value, val) 

            # Calcula max_diff para comparacion con delta
            V_new[s-1] = min_value
            #print(min_value)
            max_diff = max(max_diff, abs(V[s-1] - V_new[s-1]))

        # Actualiza valores para la siguiente iteracion
        V = V_new
        print(f'iteracion: {i}, delta: {max_diff}')
        # Compara max_diff vs delta
        if max_diff < delta:
            max_diff_value = max_diff
            break
        #print(f'iteracion: {i}')
    return V, max_iter, max_diff_value

def Intersection(lst1, lst2):
    return set(lst1).intersection(lst2)

def lao(actions, states, cost, gamma, V, delta, dict_norte, dict_sur, dict_este, dict_oeste):
    # Hipergrafo
    G = [1]
    G_n = []
    for state in G:
        for a in actions:
            for s in states:
                aux = ftran(state, s, a, dict_norte, dict_sur, dict_este, dict_oeste)
                if aux > 0:
                    print('Here')
                    G_n.append(s)

    # Z
    Z = set()
    for i in G_n:
        Z.add(i)

    # Value Iteration
    V, max_iter, max_diff_value = algo_vi(actions, Z, cost, gamma, V, delta, dict_norte, dict_sur, dict_este, dict_oeste)

    # Optimal route
    min_value = 100
    for state in Z:
        min_value = min(V[state-1], min_value)

    return G_n, Z, V, min_value


def algo_eficiente(actions, states, cost, gamma, V, delta, dict_norte, dict_sur, dict_este, dict_oeste, heuristic, s0):
    ''' Recibe un mdp board y devuelve una matriz de valores
        Algoritmo lao
    '''
    # Recibe lista de listas
    # Retorna lista de listas con valores de politica
    #print("acciones:",actions) 
    #print("estados:", states)
    #print("costo:", cost)
    #print("gamma:", gamma)
    #print("V:", V)
    #print("delta:", delta)
    #print("dict_norte", dict_norte)
    #print("dict_sur", dict_sur)
    #print("dict_este", dict_este)
    #print("dict_oeste", dict_oeste)
    #print("heuristic:", heuristic)
    #print("len heuristic:",len(heuristic))
    
    #la heuristica se inicializa en init_mdp como 0 por ahora. Esto para cada estado
    
    #se inicializa frontera con el primer estado
    list_frontera = list()
    list_frontera.append(s0)
    #print(list_frontera)
    #print(list_frontera[0])
    
    #se inicializa el expandido vacio
    list_expandido = list()
    #print("tipo expandido:",type(list_expandido))
    
    #se inicializa el hipergrafo de conectividad
    list_hiperC = list_frontera+list_expandido
    #print("grafo de hiperconectividad",list_hiperC)
    
    #se inicializa el hipergrafo de conectividad goloso
    list_hiperG = list()
    list_hiperG.append(s0)
    #print(list_hiperG)

    #Intersection
    intersect = list(Intersection(list_frontera, list_hiperG))
    q_intersect = len(intersect)
    #print("cantidad estados en interseccion", q_intersection)
    #bucle: para cuando no exista estado s E (list_frontera interseccion list_G)
    while q_intersect > 0:
        
        #print("cantidad de elementos", q_intersect)        
        #q_intersect =-1
        
        #seleccionamos al azar un estado de la interseccion
        s_random = random.choice(intersect)
        #print("s_random:", s_random)
        #q_intersect =-1

        #eliminamos el estado random de la frontera
        list_frontera.remove(s_random)
        print("frontera sin s  random", list_frontera)
        
        #agregar en la frontera los hijos del estado random removido 
        #print(dict_este)        
        #x = s_random
        #s_random = 1
        #s_random = 55
        list_hijos_norte = [k2 for (k1, k2), _ in dict_norte.items() if k1 == s_random]
        #print(list_hijos_norte)
        list_hijos_sur = [k2 for (k1, k2), _ in dict_sur.items() if k1 == s_random]
        #print(list_hijos_sur)  
        list_hijos_este = [k2 for (k1, k2), _ in dict_este.items() if k1 == s_random]
        #print(list_hijos_este)  
        list_hijos_oeste = [k2 for (k1, k2), _ in dict_oeste.items() if k1 == s_random]
        #print(list_hijos_oeste)  
        #lista de hijos(X) que no estan en list_expandido y tienen accion
        list_hijos_aux = list_hijos_norte+list_hijos_sur+list_hijos_este+list_hijos_oeste
        #print(list_hijos_aux)
        list_hijos = list()
        for i in list_hijos_aux:
            if i not in list_hijos:
                list_hijos.append(i)
        #if s_random is list_hijos:
            #list_hijos.remove(s_random) #remuevo al padre de esa lista en caso exista
        #unirlos a la list_frontera
        list_frontera = list_frontera+list_hijos
        list_frontera.remove(s_random)
        #if s_random in list_frontera:
        #    list_frontera.remove(s_random)        
        #else:
        #    pass
        print("list_frontera", list_frontera)
        #agrego el estado s al conjunto de expandidos
        list_expandido.append(s_random)
        print("list_expandido", list_expandido)
        #hipergrafo de conectividad = I(list_frontera) union F(list_expandido)
        list_hiperC = list_expandido+list_frontera
        print("list_hiperC", list_hiperC)
        #z
        list_z = list_frontera.copy()
        list_z.append(s_random)
        #
        print("list_z",list_z)
        
        #
        #VI


        #
        
        q_intersect =-1  #parada de prueba
        #intersect = list(Intersection(list_frontera, list_hiperG))
        #q_intersect = len(intersect)


    return 0

if __name__ == '__main__':
    delta = 0.001
    ambiente = 1
    dict_norte, dict_sur, dict_este, dict_oeste = init_ftran(ambiente)
    actions, states, cost, gamma, V, delta, heuristic = init_mdp(ambiente, delta)
    #V, max_iter, max_diff = algo_vi(actions, states, cost, gamma, V, delta, dict_norte, dict_sur, dict_este, dict_oeste)
    #print(V)
    ####LAO*
    #s0 = 1 #estado inicial por defecto
    #algo_eficiente(actions, states, cost, gamma, V, delta, dict_norte, dict_sur, dict_este, dict_oeste, heuristic, s0)
    G, Z, V, min_value = lao(actions, states, cost, gamma, V, delta, dict_norte, dict_sur, dict_este, dict_oeste)
    print("cascada")
