def init_mdp(type: str):
    ''' Inicializa mdp: estados, recompensas, transicion, heuristicas
        type: "5x25", "20x100", "50x250"
    '''
    # actions
    # states
    # rewards
    # heuristics
    # transition
    # initial state

    # Debe retornar un grafo (lista de listas)
    return 0

def algo_vi(mdp: str):
    ''' Recibe un mdp board y devuelve una matriz de valores
        Algoritmo value iteration
    '''
    # Recibe lista de listas
    # Retorna lista de listas con valores de politica
    return 0

def algo_eficiente(mdp: str):
    ''' Recibe un mdp board y devuelve una matriz de valores
        Algoritmo lao
    '''
    # Recibe lista de listas
    # Retorna lista de listas con valores de politica
    return 0

if __name__ == '__main__':
    # Setup variables
    type = ""
    # inicializar mdp
    mdp = init_mdp(type)
    # Prueba algoritmo eficiente
    algo_eficiente("mdp")
    # Prueba algoritmo vi
    algo_vi("mdp")
    print("cascada")
