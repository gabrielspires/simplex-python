# // 2 			    Nº de variaveis
# // 2			    Nº de restrições (exceto as de nao negatividade)
# // 1 0			Indica se as variáveis são não negativas ou livres (x>=0 ou sem restrição de nao negatividade)
# // 1 1			Coeficientes da função objetivo
# // 1 -1 <= 2	    Restrições
# // 1 1 >= 1		Restrições

# // (a)  Ler a entrada
# // (b)  Transforma-la em FPI
# // (c)  Rodar a PL auxiliar para encontrar uma base e verificar se o problema é viável
# // (este passo pode ser pulado caso você identifique uma base ́obvia).
# // (d)  Se o problema for viável, rodar o Simplex e ou encontrar a solução ́otima, ou
# // verificar que o problema é ilimitado.
# // (e)  Ao final, deve escrever um arquivo de saída. Será dado 1 ponto extra para quem
# // incluir certificados no arquivo de saída.

from sys        import argv
from fractions  import Fraction
from copy       import deepcopy
import numpy    as np
from simplex import Simplex
from utils import getEntry


def printa_cOiSaS(FPIMatrix):
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
                print("%2d" % FPIMatrix[i,j].numerator, '\t', sep="", end="")
            else:
                print(FPIMatrix[i,j].numerator, '/', FPIMatrix[i,j].denominator, '\t', sep="", end="")
        if i == 0: print(" | <- (C|VO)")
        else: print(" | <- (A|b)")
    # print("==========================================")


def AssembleTableau(FPIMatrix, basis):    
    # Adiciona a matriz de operações na PL
    zeros = np.zeros((1, FPIMatrix.shape[0]-1), dtype='object')
    identityMatrix = np.identity(FPIMatrix.shape[0]-1, dtype='object')
    operationMatrix = np.concatenate((zeros,identityMatrix), axis=0)
    tableau = np.concatenate((operationMatrix, FPIMatrix), axis=1)    

    # Multiplica o vetor c por -1
    tableau[0,:] *= -1
    return tableau


# adiciona zeros na coluna das bases criadas ao se adicionar as variaveis de folga
def AddZeros(restrictions, numVariables, slackVar, objFunction):
    # Adiciona uma coluna na posição numVariables da função objetiva
    objFunction.insert(numVariables, 0)
    # Para todas as posições exceto o 1 que adicionamos, coloque zero
    for j in range(len(restrictions)):
        if j is not slackVar:
            # print(j,restrictions[j], end="\n")
            restrictions[j].insert(numVariables, 0)
            # print(j,restrictions[j], end="\n\n")


# Lê o arquivo de entrada e cospe uma matriz em FPI
def ReadInput(inputFile):
    numVariables    = int(inputFile.readline())
    numRestrictions = int(inputFile.readline())

    nonNegativity = inputFile.readline().split()
    objFunction   = inputFile.readline().split()

    basisColumns = []

    numSlackVar = 0

    # Converte em uma lista de float
    objFunction = list(map(float, objFunction))

    # Cria uma lista vazia com o mesmo número de posições que restrições do problema 
    # Cada posição será uma lista com os elementos da restrição lida do arquivo
    restrictions = [0] * numRestrictions

    # Lê as linhas do arquivo contendo as restriçoes
    # Cada restrição fica em uma posição da lista (vira uma lista de listas)
    for i in range(numRestrictions):
        restrictions[i] = inputFile.readline().split()
        
    # Substitui as variáveis sem restrição de não-negatividade
    numFreeVar = 0
    for i in range(len(nonNegativity)):
        positive = int(nonNegativity[i])
        if not positive:
            # É uma variável livre
            numFreeVar += 1
            numVariables += 1
            # if objFunction[i] is not 0:
            objFunction.insert(i+numFreeVar, objFunction[i+numFreeVar-1]*-1)
            for j in range(len(restrictions)):
                # if int(restrictions[j][i]) is not 0:
                restrictions[j].insert(i+numFreeVar, int(restrictions[j][i+numFreeVar-1])*-1)
    
    # Adiciona o valor objetivo 0 na função objetiva
    objFunction.append(Fraction(0))

    # Adiciona as variáveis de folga
    for i in range(len(restrictions)):
        # print(restrictions[i], '\n')
        if restrictions[i][numVariables] == '<=':
            # Adiciona variável de folga positiva
            restrictions[i].remove('<=')
            # restrictions[i][numVariables] = 1
            # AddZeros(restrictions, numVariables, i, objFunction)
            # basisColumns.append(numVariables)
            # numVariables += 1
            # numSlackVar += 1
        elif restrictions[i][numVariables] == '>=':
            # Adiciona variável de folga negativa
            #restrictions[i][numVariables] = -1
            # AddZeros(restrictions, numVariables, i, objFunction)
            restrictions[i].remove('>=')
            restrictions[i] = [float(x)*-1 for x in restrictions[i]]
            # basisColumns.append(numVariables)
            # numVariables += 1
            # numSlackVar += 1
        elif restrictions[i][numVariables] == '==':
            # Remove o sinal, já que não é preciso adicionar nada
            # restrictions[i][numVariables] == 0
            # restrictions[i].remove('==')
            restrictions[i][numVariables] = -1
            AddZeros(restrictions, numVariables, i, objFunction)
            numVariables += 1

    # for i in range(len(restrictions)):
    #     print(restrictions[i])

    # Converte as listas em fractions
    objFunction = [int(x) for x in objFunction]
    # objFunction.insert(-1, Fraction(0))
    objFunction = np.array(objFunction)
    for i in range(len(restrictions)):
        restrictions[i] = [float(x) for x in restrictions[i]]

    # Cria a matrix da PL
    FPIMatrix = []

    # Coloca as restrições na matrix (tudo na mesma linha pq é mais fácil)
    for i in range(len(restrictions)):
        FPIMatrix.append(restrictions[i])

    # Insere a função objetiva antes da primeira linha
    FPIMatrix = np.insert(FPIMatrix, 0, objFunction, 0)

    return FPIMatrix, numVariables, numRestrictions


def printar(tableau):
    i,j = np.shape(tableau)
    for a in range(i):
        for b in range(j):
            print(int(tableau[a,b]), "\t", end='')
        print()


simplex = Simplex()


def main():
    inputFile = open(argv[1])
    outputFile = open(argv[2], "w")
    
    # Monta a PL em FPI
    FPIMatrix, numVariables, numRestrictions = ReadInput(inputFile)

    aux = "["
    #print(numRestrictions)
    #print(numVariables)

    for list in range(len(FPIMatrix)):
        aux += "[%s" % ",".join([str(i) for i in FPIMatrix[list]]) + "]"
        if list < len(FPIMatrix)-1:
            aux += ","
    aux += "]"
    # print(aux)
    simplex.init(aux, numRestrictions, numVariables)

if __name__ == '__main__':
    main()