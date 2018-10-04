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
import numpy as np


def ReadInput(inputFile):
    # Lê o conteúdo do arquivo
    numVariables    = int(inputFile.readline())
    numRestrictions = int(inputFile.readline())

    nonNegativity = inputFile.readline().split()
    objFunction   = inputFile.readline().split()

    # Converte em uma lista de inteiros
    objFunction = list(map(int, objFunction))

    restrictions = [0] * numRestrictions

    for i in range(numRestrictions):
        restrictions[i] = inputFile.readline().split()

    print("========================")
    print("numVar:", numVariables, "numRestr:", numRestrictions)
    print("non neg", nonNegativity)
    print("obj func:", objFunction)
    print("restric.:", restrictions)
    print("========================")

    # Substitui as variáveis sem restrição de não-negatividade
    for i in range(len(nonNegativity)):
        isPositive = int(nonNegativity[i])
        if not isPositive:
            print("É zero, substituir por x^+ - x^- (uma variavel a mais)!")
            numVariables += 1
            if objFunction[i] > 0:
                objFunction.insert(i+1, objFunction[i]*-1)
            for j in range(len(restrictions)):
                if int(restrictions[j][i]) is not 0:
                    restrictions[j].insert(i+1, int(restrictions[j][i])*-1)

    print("========================")
    print("numVar:", numVariables, "numRestr:", numRestrictions)
    print("non neg", nonNegativity)
    print("obj func:", objFunction)
    for i in range(len(restrictions)): print("restric.:", restrictions[i])
    print("========================")

    # Adiciona as variáveis de folga
    for i in range(len(restrictions)):
        if restrictions[i][numVariables] == '<=':
            # Adiciona variável de folga positiva
            restrictions[i][numVariables] = 1
            numVariables += 1
        if j == '>=':
            # Adiciona variável de folga negativa
            restrictions[i][numVariables] = 1
            numVariables += 1
        # if j == '==':

    print("========================")
    print("numVar:", numVariables, "numRestr:", numRestrictions)
    print("non neg", nonNegativity)
    print("obj func:", objFunction)
    for i in range(len(restrictions)): print("restric.:", restrictions[i])
    print("========================")


def main():
    inputFile = open(argv[1])
    outputFile = open(argv[2], "w")
    
    ReadInput(inputFile)
    

if __name__ == '__main__':
    main()