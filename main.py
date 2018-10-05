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

from sys        import argv
from fractions  import Fraction
import numpy    as np


def printa_cOiSaS(FPIMatrix):
    numRows, numColumns = FPIMatrix.shape
    numColumns -= 1

    print("==========================================")
    print("    ", end = '')
    for i in range(numColumns): print("%2d" % i, "\t", end='')
    print()
    for i in range(numRows):
        print(i, "| ", end="")
        for j in range(numColumns+1):
            if (FPIMatrix[i,j].denominator == 1):
                print("%2d" % FPIMatrix[i,j].numerator, '\t', sep="", end="")
            else:
                print(FPIMatrix[i,j].numerator, '/', FPIMatrix[i,j].denominator, '\t', sep="", end="")
        if i == 0: print(" | <- (C|VO)")
        else: print(" | <- (A|b)")
    print("==========================================")

# adiciona zeros na coluna das bases criadas ao se adicionar as variaveis de folga
def AddZeros(restrictions, numVariables, slackVar, objFunction):
    # Adiciona uma coluna na posição numVariables da função objetiva
    objFunction.insert(numVariables, 0)
    # Para todas as posições exceto o 1 que adicionamos, coloque zero
    for j in range(len(restrictions)):
        if j is not slackVar:
            restrictions[j].insert(numVariables-1, 0)
    
# Lê o arquivo de entrada e cospe uma matriz em FPI
def ReadInput(inputFile):
    numVariables    = int(inputFile.readline())
    numRestrictions = int(inputFile.readline())

    nonNegativity = inputFile.readline().split()
    objFunction   = inputFile.readline().split()

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
    for i in range(len(nonNegativity)):
        isPositive = int(nonNegativity[i])
        if not isPositive:
            # É uma variável livre
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
            # Remove o sinal, já que não é preciso adicionar nada
            restrictions[i].remove('==')

    # Converte as listas em fractions
    objFunction = [Fraction(x) for x in objFunction]
    objFunction.insert(-1, Fraction(0))
    objFunction = np.array(objFunction)
    for i in range(len(restrictions)):
        restrictions[i] = [Fraction(x) for x in restrictions[i]]

    # Cria a matrix da PL
    FPIMatrix = []

    # Coloca as restrições na matrix (tudo na mesma linha pq é mais fácil)
    for i in range(len(restrictions)):
        FPIMatrix += restrictions[i]

    # Converte em matriz do numpy
    FPIMatrix = np.matrix(FPIMatrix)

    # Transforma a matrix p/ ter as dimensões corretas
    FPIMatrix = FPIMatrix.reshape(numRestrictions, numVariables+1)

    # Insere a função objetiva antes da primeira linha
    FPIMatrix = np.insert(FPIMatrix, 0, objFunction, 0)

    # Fecha o arquivo de entrada e retorna a PL
    inputFile.close()
    return FPIMatrix


def main():
    inputFile = open(argv[1])
    outputFile = open(argv[2], "w")
    
    FPIMatrix = ReadInput(inputFile)
    printa_cOiSaS(FPIMatrix)

if __name__ == '__main__':
    main()