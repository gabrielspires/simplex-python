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
    numVariables    = int(inputFile.readline())
    numRestrictions = int(inputFile.readline())
    print(numVariables, numRestrictions)

    nonNegativity = inputFile.readline().split()

    for i in nonNegativity:
        isNonNegative = int(i)
        if isNonNegative:
            print("É um, então tudo bem!")
        else:
            print("É zero, substituir por x^+ - x^- (uma variavel a mais)!")
            numVariables += 1
    
    
    print(nonNegativity)

def main():
    inputFile = open(argv[1])
    outputFile = open(argv[2], "w")
    
    ReadInput(inputFile)
    

if __name__ == '__main__':
    main()