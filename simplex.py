from utils import printConclusao
from utils import printPivoting
from fractions import Fraction
from matrix import Matrix
import numpy as np

# facilita a seleção das opções
NONVIABLE = 0
UNBOUNDED = 1
LIMITED = 2


class simplex():
    # instância da PL que será usada
    matrix = Matrix()
    # flag que indica se a PL é a original ou a auxiliar
    auxiliary = False

    def init(self, tableau, numSlackVar):
        # self.matrix.init(m, r, c)
        # self.matrix.tableau()
        # self.selection()
         self.matrix = Matrix(tableau, numSlackVar)

    # função chave do trabalho: verifica o tableau a cada etapa e indica o que deverá ser feito a seguir
    def selection(self):
        c = True
        b = True

        # verifica se existe -c negativo
        for i in range(0, self.matrix.getC().shape[1]):
            if(self.matrix.getC()[0, i] < 0):
                c = False
                break

        # verifica se existe b negativo
        for i in range(1, self.matrix.getB().shape[0]):
            if(self.matrix.getB()[i, 0] < 0):
                b = False
                break

        # -c positivo e b negativo: testa se não há um caso de invialibilidade e escolhe fazer o dual simplex
        if(c is True and b is False):
            (index, valid) = self.testNonViable()
            if(valid is True):
                self.dual()
            else:
                self.nonViable(index)
        # -c negativo e b positivo: testa se não há um caso de ilimitada na PL original e escolhe fazer o simplex primal
        elif(c is False and b is True):
            if(self.auxiliary is False):
                (index, valid) = self.testUnbounded()
            else:
                valid = True
            if(valid is True):
                self.primal()
            else:
                self.unbounded(index)
        # -c negativo e b negativo: necessário ajustar as entradas do b e fazer a PL auxiliar
        elif(c is False and b is False):
            self.auxiliary = True
            self.adjustMatrix()
        # -c positivo e b positivo: situação de tableau ótimo (garantindo que sempre se tem uma base viável de soluções)
        elif(c is True and b is True):
            # se chegou ao fim do simplex para PL auxiliar, avalia o que aconteceu com ela
            if(self.auxiliary is True):
                self.evalAuxiliary()
            else:
                self.end()
