# // 2 			Nº de variaveis
# // 2			Nº de restrições (exceto as de nao negatividade)
# // 1 0			Indica se as variáveis são não negativas ou livres (x>=0 ou sem restrição de nao negatividade)
# // 1 1			Coeficientes da função objetivo
# // 1 -1 <= 2	Restrições
# // 1 1 >= 1		Restrições

# // (a)  Ler a entrada
# // (b)  Transforma-la em FPI
# // (c)  Rodar a PL auxiliar para encontrar uma base e verificar se o problema é viável
# // (este passo pode ser pulado caso você identifique uma base ́obvia).
# // (d)  Se o problema for viável, rodar o Simplex e ou encontrar a solução ́otima, ou
# // verificar que o problema é ilimitado.
# // (e)  Ao final, deve escrever um arquivo de sa ́ıda. Ser ́a dado 1 ponto extra para quem
# // incluir certificados no arquivo de saída.

from sys import argv
from fractions import Fraction
import numpy as np


def printa_cOiSaS(numVariables, numRestrictions, nonNegativity, objFunction, restrictions):
    print("==========================================")
    print("numVar:", numVariables, "numRestr:", numRestrictions)
    print("Variáveis com restrição de nao-neg:", nonNegativity)
    print("[ ", end="")
    for i in range(len(objFunction)): print("%2d" % objFunction[i].numerator, '/', objFunction[i].denominator, ", ", sep="", end="")
    print(" ] <- C")
    for i in range(len(restrictions)):
        print("[ ", end="")
        for j in range(len(restrictions[i])):
            #print("%3.1f" % restrictions[i][j], ",", sep="", end="")
            print("%2d" % restrictions[i][j].numerator, '/', restrictions[i][j].denominator, ', ', sep="", end="")
        print(" ] <- (A|b)")
    print("==========================================")


def AddZeros(restrictions, numVariables, i, objFunction):
    objFunction.insert(numVariables, 0)
    for j in range(len(restrictions)):
        if j is not i:
            restrictions[j].insert(numVariables-1, 0)
    

def ReadInput(inputFile):
    # Lê o conteúdo do arquivo
    numVariables    = int(inputFile.readline())
    numRestrictions = int(inputFile.readline())

    nonNegativity = inputFile.readline().split()
    objFunction   = inputFile.readline().split()

    # Converte em uma lista de inteiros
    objFunction = list(map(float, objFunction))

    restrictions = [0] * numRestrictions

    for i in range(numRestrictions):
        restrictions[i] = inputFile.readline().split()

    # Substitui as variáveis sem restrição de não-negatividade
    for i in range(len(nonNegativity)):
        isPositive = int(nonNegativity[i])
        if not isPositive:
            print("É zero, substituir por x^+ - x^- (uma variavel a mais)!")
            numVariables += 1
            if objFunction[i] is not 0:
                objFunction.insert(i+1, objFunction[i]*-1)
            for j in range(len(restrictions)):
                if int(restrictions[j][i]) is not 0:
                    restrictions[j].insert(i+1, str(int(restrictions[j][i])*-1))

    # Adiciona as variáveis de folga
    for i in range(len(restrictions)):
        if restrictions[i][-2] == '<=':
            # Adiciona variável de folga positiva
            restrictions[i][-2] = 1
            numVariables += 1
            AddZeros(restrictions, numVariables, i, objFunction)
        elif restrictions[i][-2] == '>=':
            # Adiciona variável de folga negativa
            restrictions[i][-2] = -1
            numVariables += 1
            AddZeros(restrictions, numVariables, i, objFunction)
        elif restrictions[i][-2] == '==':
            restrictions[i].remove('==')

    # Converte as listas em fractions
    objFunction = [Fraction(x) for x in objFunction]
    objFunction.insert(-1, Fraction(0))
    objFunction = np.array(objFunction)
    for i in range(len(restrictions)):
        restrictions[i] = [Fraction(x) for x in restrictions[i]]

    # printa_cOiSaS(numVariables, numRestrictions, nonNegativity, objFunction, restrictions)

    FPIMatrix = []
    for i in range(len(restrictions)):
        FPIMatrix += restrictions[i]

    FPIMatrix = np.matrix(FPIMatrix)
    FPIMatrix = FPIMatrix.reshape(numRestrictions, numVariables+1)
    print(FPIMatrix)
    print("asdasd")
    FPIMatrix = np.insert(FPIMatrix, 0, objFunction, 0)

    print(FPIMatrix)

def main():
    inputFile = open(argv[1])
    outputFile = open(argv[2], "w")
    
    ReadInput(inputFile)
    

if __name__ == '__main__':
    main()