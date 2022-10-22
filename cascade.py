import numpy as np
import pandas as pd

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
        cost = [1] * 5*25
        cost[101] = 0
    elif ambiente == 2:
        cost = [1] * 20*100
        cost[1901] = 0
    elif ambiente == 3:
        cost = [1] * 50*250
        cost[12251] = 0
    else:
        cost = 0
        print("Error en la asignacion de costos")

    # estado inicial
    if ambiente == 1:
        V = [0] * 5*25
    elif ambiente == 2:
        V = [0] * 5*25
    elif ambiente == 3:
        V = [0] * 5*25
    else:
        V = 0
        print("Error en los valores iniciales")

    # gamma / factor de descuento
    gamma = 1

    # delta
    delta = delta_value
    return actions, states, cost, gamma, V, delta

def init_ftran(ambiente: int):
    PATH = f'Ambientes/Ambiente{ambiente}'
    df_norte = pd.read_csv(f'{PATH}/Action_Norte.txt', sep="   ", header=None)
    df_este = pd.read_csv(f'{PATH}/Action_Este.txt', sep="   ", header=None)
    df_oeste = pd.read_csv(f'{PATH}/Action_Oeste.txt', sep="   ", header=None)
    df_sur = pd.read_csv(f'{PATH}/Action_Sur.txt', sep="   ", header=None)
    df_norte.columns = ['s', 's_next', 'p']
    df_este.columns = ['s', 's_next', 'p']
    df_oeste.columns = ['s', 's_next', 'p']
    df_sur.columns = ['s', 's_next', 'p']
    #df_list = [df_este, df_oeste, df_norte, df_sur]

    df_norte = df_norte.astype({'s':'int'})
    df_norte = df_norte.astype({'s_next':'int'})
    df_este = df_este.astype({'s':'int'})
    df_este = df_este.astype({'s_next':'int'})
    df_oeste = df_oeste.astype({'s':'int'})
    df_oeste = df_oeste.astype({'s_next':'int'})
    df_sur = df_sur.astype({'s':'int'})
    df_sur = df_sur.astype({'s_next':'int'})
    return df_este, df_oeste, df_norte, df_sur

def ftran(s: int, s_next: int, a: int, df_este: pd.DataFrame,
                                       df_oeste: pd.DataFrame,
                                       df_norte: pd.DataFrame,
                                       df_sur: pd.DataFrame) -> float:
    ''' ftran
        Recibe s, s', a (estado inicial, final y accion) y los dataframes
    '''
    # 1: este, 2: oeste, 3: norte, 4: sur
    if a == 1:
        df_new = df_este[df_este['s'] == s][df_este['s_next'] == s_next]
        if df_new.shape[0] == 0:
            return 0
        elif df_new.shape[0] == 1:
            return df_new['p'].values[0]
        else:
            print('ERROR EN LA FUNCION DE TRANSICION')
            return 0
    if a == 2:
        df_new = df_oeste[df_oeste['s'] == s][df_oeste['s_next'] == s_next]
        if df_new.shape[0] == 0:
            return 0
        elif df_new.shape[0] == 1:
            return df_new['p'].values[0]
        else:
            print('ERROR EN LA FUNCION DE TRANSICION')
            return 0
    if a == 3:
        df_new = df_norte[df_norte['s'] == s][df_norte['s_next'] == s_next]
        if df_new.shape[0] == 0:
            return 0
        elif df_new.shape[0] == 1:
            return df_new['p'].values[0]
        else:
            print('ERROR EN LA FUNCION DE TRANSICION')
            return 0
    if a == 4:
        df_new = df_sur[df_sur['s'] == s][df_sur['s_next'] == s_next]
        if df_new.shape[0] == 0:
            return 0
        elif df_new.shape[0] == 1:
            return df_new['p'].values[0]
        else:
            print('ERROR EN LA FUNCION DE TRANSICION')
            return 0

def algo_vi(actions, states, cost, gamma, V, delta, df_este, df_oeste, df_norte, df_sur):
    ''' algo_vi
        Recibe acciones, estados, costo, gamma y valores V, corre el algo
        value iteration y devuelve la lista de valores para los estados
    '''
    max_iter = 10000
    for i in range (max_iter):
        max_diff = 1
        V_new = V.copy()
        for s in states:
            min_value = 100
            for a in actions:
                val = cost[s-1]
                for s_next in states:
                    val += ftran(s, s_next, a, df_este, df_oeste, df_norte, df_sur) * (gamma * V[s_next-1])

                # Min value
                min_value = min(min_value, val) 

            # Calcula max_diff para comparacion con delta
            V_new[s-1] = min_value
            max_diff = max(max_diff, abs(V[s-1] - V_new[s-1]))

        # Actualiza valores para la siguiente iteracion
        V = V_new

        # Compara max_diff vs delta
        if max_diff < delta:
            break
        print(i)
        print(max_diff)
    return V, max_iter

def algo_eficiente(mdp: str):
    ''' Recibe un mdp board y devuelve una matriz de valores
        Algoritmo lao
    '''
    # Recibe lista de listas
    # Retorna lista de listas con valores de politica
    return 0

if __name__ == '__main__':
    ambiente = 1
    df_este, df_oeste, df_norte, df_sur = init_ftran(ambiente)
    actions, states, cost, gamma, V, delta = init_mdp(ambiente, 0.001)
    V, max_iter = algo_vi(actions, states, cost, gamma, V, delta, df_este, df_oeste, df_norte, df_sur)
    print("cascada")
