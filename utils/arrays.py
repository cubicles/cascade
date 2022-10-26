

# Creates a list containing 5 lists, each of 8 items, all set to 0
# w = columnas
# h = filas
w, h = 8, 5
Matrix = [[0 for x in range(w)] for y in range(h)] 

for j in range(w):
    for i in range(h):
        print(f'Fila:{i+1},Columna:{j+1}')
        print(Matrix[i][j])

class matrix:
    def __init__(self, n, m):
        self.matrix = self.get_matrix(n, m)

    def get_matrix(

    def set_value(self, filas: int, columnas: int, value: float):
        #self.matrix[[filas-1][columnas-1]] = value
        return 0

    def get_value(self, filas: int, columnas: int) -> float:
        return self.matrix[[filas-1][columnas-1]]


def fill(matrix, fila, columna):
    matrix[][]


if __name__ == '__main__':
    board = matrix(4, 4)
    test = [[0 for x in range(8)] for y in range(5)] 



