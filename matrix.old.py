from fractions  import Fraction
import numpy    as np
from copy       import deepcopy


# Tableau
# Tableau aux
# Lista de bases


class Matrix:
    tableau_original = None
    tableau_aux = None
    aux = False
    basis = []
    slackVar = None
    A = None
    b = None
    c = None

    def __init__(self, tableau, slackVar):
        self.slackVar = slackVar
        self.updateFractions(tableau)

        self.tableau_original = np.matrix(tableau, dtype="object")
        self.breakTableau()
        self.setAux()

        # self.printa_cOiSaS(self.tableau_original)
        # self.printa_cOiSaS(self.getA())
        # self.printa_cOiSaS(self.getB())
        # self.printa_cOiSaS(self.getC())
        # self.printa_cOiSaS(self.getOpMatrix())
        # self.printa_cOiSaS(self.getSlack())
        # self.printa_cOiSaS(self.tableau_original)
        # self.printa_cOiSaS(self.tableau_original)
        # nmero variapveis --> bases = [(0,0), (1,0), (2,0)]
        # self.table

        # fazer tableau orig
        # fazer tableu da PL aux
    
    # dada uma posição no tableau_aux (linha, coluna), pivoteia o elemento nessa posição
    def pivoting(self, row, col):
        if not self.aux:
            # calcula por quanto a linha do pivô será multiplicada para que ele seja 1
            multiplier = Fraction(1, self.tableau_original[row, col])

            # atualiza os elementos na linha do pivô
            for i in range(0, self.tableau_original.shape[1]):
                self.tableau_original[row, i] = self.tableau_original[row, i] * multiplier

            # atualiza restante da matriz
            for i in range(0, self.tableau_original.shape[0]):
                if i != row:
                    multiplier = -1 * Fraction(self.tableau_original.T[col, i], self.tableau_original.T[col, row])
                    for j in range(0, self.tableau_original.shape[1]):
                        self.tableau_original[i, j] = self.tableau_original[i, j] + self.tableau_original[row, j] * multiplier

            # atualiza lista de bases considerando a nova base encontrada
            self.updateBase(row, col)

            print('pivot tableau original', self.basis)
            self.printa_cOiSaS(self.tableau_original)
        else:
            # calcula por quanto a linha do pivô será multiplicada para que ele seja 1
            multiplier = Fraction(1, self.tableau_aux[row, col])

            # atualiza os elementos na linha do pivô
            for i in range(0, self.tableau_aux.shape[1]):
                self.tableau_aux[row, i] = self.tableau_aux[row, i] * multiplier

            # atualiza restante da matriz
            for i in range(0, self.tableau_aux.shape[0]):
                if i != row:
                    multiplier = -1 * Fraction(self.tableau_aux.T[col, i], self.tableau_aux.T[col, row])
                    for j in range(0, self.tableau_aux.shape[1]):
                        self.tableau_aux[i, j] = self.tableau_aux[i, j] + self.tableau_aux[row, j] * multiplier

            # atualiza lista de bases considerando a nova base encontrada
            self.updateBase(row, col)

            print('pivot tableau auxiliar', self.basis)
            self.printa_cOiSaS(self.tableau_aux)


    # dada uma posição no tableau (linha, coluna), atualiza a lista de bases
    def updateBase(self, row, col):
        for i in self.basis:
            if(i[0] == row):
                i[1] = col
                break


    # passa todos os valores para Fraction (facilitar cálculos e garantir precisão nas contas)
    def updateFractions(self, tableau):
        for i in range(0, tableau.shape[0]):
            for j in range(0, tableau.shape[1]):
                tableau[i, j] = Fraction(tableau[i, j])


    def setAux(self):
        # print('tableau original')
        # self.printa_cOiSaS(self.tableau_original)

        # Cria uma linha de zeros
        C = np.zeros((1, self.tableau_original.shape[1]-1))
        # Pega todas as linhas do tableau menos a primeira
        A = np.matrix(self.tableau_original[1:,:-1])

        # Concatena a primeira linha com o resto da matrix
        self.tableau_aux = np.concatenate((C, A), axis=0)
        
        idMatTop = np.ones((1, self.tableau_aux.shape[0]-1))
        idMat = np.identity(self.tableau_aux.shape[0]-1)
        
        idMat = np.concatenate((idMatTop, idMat), axis=0)
        idMat = np.concatenate((idMat, self.tableau_original[:,-1]), axis=1)
        self.tableau_aux = np.concatenate((self.tableau_aux, idMat), axis=1)
        self.updateFractions(self.tableau_aux)

        # adiciona as novas bases na lista de bases
        for i in range(0, self.getSlack().shape[0]):
            for j in range(0, self.getSlack().shape[1]):
                if(self.getSlack()[i, j] == 1):
                    self.basis.append([i + 1, 2*self.A.shape[0] + self.c.shape[1] + j])

        # print('tableau aux')
        # self.printa_cOiSaS(self.tableau_aux)
        # print(self.basis)
        # self.printa_cOiSaS(self.getA())
        # print(self.getB())
        # print(self.getC())
        # self.printa_cOiSaS(self.getOpMatrix())
        # self.printa_cOiSaS(self.getSlack())

    def setAux2(self):
        # print('tableau original')
        # self.printa_cOiSaS(self.tableau_original)

        # Cria uma linha de zeros
        C = np.zeros((1, self.tableau_aux.shape[1] - 1))
        # Pega todas as linhas do tableau menos a primeira
        A = np.matrix(self.tableau_aux[1:, :-1])

        # Concatena a primeira linha com o resto da matrix
        self.tableau_aux = np.concatenate((C, A), axis=0)

        idMatTop = np.ones((1, self.tableau_aux.shape[0] - 1))
        idMat = np.identity(self.tableau_aux.shape[0] - 1)

        idMat = np.concatenate((idMatTop, idMat), axis=0)
        idMat = np.concatenate((idMat, self.tableau_aux[:, -1]), axis=1)
        self.tableau_aux = np.concatenate((self.tableau_aux, idMat), axis=1)
        self.updateFractions(self.tableau_aux)

        # adiciona as novas bases na lista de bases
        for i in range(0, self.getSlack().shape[0]):
            for j in range(0, self.getSlack().shape[1]):
                if (self.getSlack()[i, j] == 1):
                    self.basis.append([i + 1, 2 * self.A.shape[0] + self.c.shape[1] + j])


    def printa_cOiSaS(self, FPIMatrix):
        numRows, numColumns = FPIMatrix.shape
        numColumns -= 1

        # print("==========================================")
        # print("    ", end = '')
        # for i in range(numColumns): print("%2d" % i, "\t", end='')
        # print()
        for i in range(numRows):
            # print(i, "| ", end="")
            for j in range(numColumns+1):
                if (FPIMatrix[i,j].denominator == 1):
                    print("\t", FPIMatrix[i,j].numerator, sep="", end="")
                else:
                    print("\t", FPIMatrix[i,j].numerator, '/', FPIMatrix[i,j].denominator, sep="", end="")
            if i == 0: print(" | <- (C|VO)")
            else: print(" | <- (A|b)")
        # print("==========================================")

    def breakTableau(self):
        self.c = self.tableau_original[0, self.slackVar:-(self.slackVar+1)]
        self.A = self.tableau_original[1:,self.slackVar:-(self.slackVar+1)]
        self.b = self.tableau_original[:,-1]

    # retorna a matriz A (A + folgas) atualizado
    def getA(self):
        if not self.aux:
            return self.tableau_original[1:, self.A.shape[0]:-1]
        else:
            return self.tableau_aux[1:, self.A.shape[0]:-1]

    # retorna o vetor b (b + valor objetivo) atualizado
    def getB(self):
        if not self.aux:
            return self.tableau_original[:, -1]
        else:
            return self.tableau_aux[:, -1]

    # retorna o vetor -c (-c + custo das folgas) atualizado
    def getC(self):
        if not self.aux:
            return self.tableau_original[0, self.A.shape[0]:-1]
        else:
            return self.tableau_aux[0, self.A.shape[0]:-1]

    # retorna a matriz "memória" (certificado + matriz de registros)
    def getOpMatrix(self):
        if not self.aux:
            return self.tableau_original[:, 0:self.A.shape[0]]
        else:
            return self.tableau_aux[:, 0:self.A.shape[0]]

    # retorna a matriz de folgas (desconsiderando seu custo, já incluso no -c)
    def getSlack(self):
        if not self.aux:
            return self.tableau_original[1:, -(self.slackVar+1):-1]
        else:
            return self.tableau_aux[1:, self.A.shape[0] + (self.getC().shape[1] - self.A.shape[0]):-1]

