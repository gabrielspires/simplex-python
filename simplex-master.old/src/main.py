from simplex import Simplex
from utils import getEntry
import numpy as np

# instância da classe principal
simplex = Simplex()

def printar(tableau):
    i,j = np.shape(tableau)
    for a in range(i):
        for b in range(j):
            print(int(tableau[a,b]), "\t", end='')
        print()

def main():
    (aux, row, col) = getEntry()
    print(type(col))
    print(type(row))
    print(type(aux))
    simplex.init(aux, row, col)
    printar(simplex.matrix.tableau)
    print('\n\n')
    simplex.matrix.extendAuxiliary()
    printar(simplex.matrix.tableau)

if __name__ == '__main__':
    main()
