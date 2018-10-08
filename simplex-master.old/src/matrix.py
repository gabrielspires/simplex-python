from fractions import Fraction
import numpy as np


# classe utilizada para guardar uma instância de uma PL (já em formato FPI e no tableau), seus elementos e seus métodos
class Matrix:
    A = 0
    b = 0
    c = 0
    tableau = 0
    base = []

    # inicializa partes importantes da matriz
    def init(self, matrix, row, col):
        aux1 = np.matrix(matrix, dtype='object')
        aux2 = aux1.reshape(row + 1, col + 1)

        # guarda as partes originais da PL
        self.A = np.matrix(aux2[1:, 0:-1], dtype='object')
        self.b = np.matrix(aux2[:, -1], dtype='object')
        self.c = np.matrix(aux2[0, 0:-1], dtype='object')

    # monta o tableau para a PL original
    def tableau(self):
        zeros = np.zeros((1, self.A.shape[0]), dtype='object')
        identity = np.identity(self.A.shape[0], dtype='object')

        # calcula -c
        c1 = -1 * self.c
        # monta vetor -c completo
        c2 = np.concatenate((zeros, c1, zeros), axis=1)
        # monta matriz A completa
        a1 = np.concatenate((identity, self.A, identity), axis=1)
        # junta -c e A
        a2 = np.concatenate((c2, a1), axis=0)
        # adiciona vetor b
        self.tableau = np.concatenate((a2, self.b), axis=1)

        self.updateFractions()

        # adiciona as novas bases na lista de bases
        for i in range(0, self.getGap().shape[0]):
            for j in range(0, self.getGap().shape[1]):
                if(self.getGap()[i, j] == 1):
                    self.base.append([i + 1, self.A.shape[0] + self.c.shape[1] + j])
        
        

    # passa todos os valores para Fraction (facilitar cálculos e garantir precisão nas contas)
    def updateFractions(self):
        for i in range(0, self.tableau.shape[0]):
            for j in range(0, self.tableau.shape[1]):
                self.tableau[i, j] = Fraction(self.tableau[i, j], 1)

    # dada uma posição no tableau (linha, coluna), atualiza a lista de bases
    def updateBase(self, row, col):
        for i in self.base:
            if(i[0] == row):
                i[1] = col
                break

    # dada uma posição no tableau (linha, coluna), pivoteia o elemento nessa posição
    def pivoting(self, row, col):
        # mensagem de erro caso não exista a posição passada
        if(row > self.tableau.shape[0] or col > self.tableau.shape[1]):
            print("Invalid position in tableau!")
            return

        # calcula por quanto a linha do pivô será multiplicada para que ele seja 1
        multiplier = Fraction(1, self.tableau[row, col])

        # atualiza os elementos na linha do pivô
        for i in range(0, self.tableau.shape[1]):
            self.tableau[row, i] = self.tableau[row, i] * multiplier

        # atualiza restante da matriz
        for i in range(0, self.tableau.shape[0]):
            if(i != row):
                multiplier = -1 * Fraction(self.tableau.T[col, i], self.tableau.T[col, row])
                for j in range(0, self.tableau.shape[1]):
                    self.tableau[i, j] = self.tableau[i, j] + self.tableau[row, j] * multiplier

        # atualiza lista de bases considerando a nova base encontrada
        self.updateBase(row, col)

    # monta tableau para PL auxiliar
    def extendAuxiliary(self):
        zeros1 = np.zeros((1, self.getC().shape[1]), dtype='object')
        ones = np.ones((1, self.getGap().shape[1]), dtype='object')
        identity = np.identity(self.A.shape[0], dtype='object')

        # monta novo -c
        c1 = np.concatenate((zeros1, ones), axis=1)
        # adiciona a identidade extra
        a1 = np.concatenate((self.getA(), identity), axis=1)
        a2 = np.concatenate((c1, a1), axis=0)
        self.tableau = np.concatenate((self.getMem(), a2, self.getB()), axis=1)
        self.updateFractions()

        # reseta a lista de bases e coloca as bases novas na lista
        self.base = []
        for i in range(0, self.getGap().shape[0]):
            for j in range(0, self.getGap().shape[1]):
                if(self.getGap()[i, j] == 1):
                    self.base.append([i + 1, self.A.shape[0] + (self.getC().shape[1] - self.A.shape[0]) + j])

    # volta para a PL original
    def destroyAuxiliary(self):
        zeros = np.zeros((1, self.A.shape[0]), dtype='object')

        # restaura -c original do tableau
        c1 = -1 * self.c
        c2 = np.concatenate((c1, zeros), axis=1)
        # concatena -c e A já excluindo a identidade da auxiliar
        aux1 = np.concatenate((c2, self.getA()[:, :-self.A.shape[0]]), axis=0)
        self.tableau = np.concatenate((self.getMem(), aux1, self.getB()), axis=1)
        self.updateFractions()

    # retorna a matriz A (A + folgas) atualizado
    def getA(self):
        return self.tableau[1:, self.A.shape[0]:-1]

    # retorna o vetor b (b + valor objetivo) atualizado
    def getB(self):
        return self.tableau[:, -1]

    # retorna o vetor -c (-c + custo das folgas) atualizado
    def getC(self):
        return self.tableau[0, self.A.shape[0]:-1]

    # retorna a matriz "memória" (certificado + matriz de registros)
    def getMem(self):
        return self.tableau[:, 0:self.A.shape[0]]

    # retorna a matriz de folgas (desconsiderando seu custo, já incluso no -c)
    def getGap(self):
        return self.tableau[1:, self.A.shape[0] + (self.getC().shape[1] - self.A.shape[0]):-1]
