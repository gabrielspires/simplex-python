from sys import argv
import numpy as np

# abre os dois arquivos de saída
pivotingFile = open("pivoting.txt", "a")
conclusaoFile = open("conclusao.txt", "w")


# resgata toda a entrada do arquivo de teste
def getEntry():
    file = open(argv[1], 'r')
    row = int(file.readline())
    col = int(file.readline())
    aux = file.readline()
    file.close()
    return aux, row, col


# manda imprimir o tableau no arquivo de pivoteamento
def printPivoting(matrix):
    printMatrixP(matrix)


# imprime a conclusão no arquivo conclusao.txt
def printConclusao(flag, certificate, optimalValue=None, solution=None):
    if flag == 0:
        print("Status: inviavel")
        print("Certificado:")
        C = np.squeeze(np.asarray(certificate))
        for x in C:
            print(float(x), end=" ")
        print()
    if flag == 1:
        print("Status: ilimitada")
        print("Certificado:")
        C = np.squeeze(np.asarray(certificate))
        for x in C:
            print(float(x), end=" ")
        print()
    if flag == 2:
        print("Status: otimo")
        print("Objetivo:", optimalValue)
        S = np.squeeze(np.asarray(solution))
        print("Solucao:")
        for x in S:
            print(float(x), end=" ")
        print()
        print("Certificado:")
        C = np.squeeze(np.asarray(certificate))
        for x in C:
            print(float(x), end=" ")
        print()


    if 0 <= flag <= 2:
        conclusaoFile.write(str(flag) + '\n')
    if flag == 2 and solution is not None:
        printMatrixC(solution)
    if flag == 2 and optimalValue is not None:
        conclusaoFile.write(np.format_float_positional(float(optimalValue), precision=5) + '\n')
    printMatrixC(certificate)

    # fecha os dois arquivos usados na execução
    pivotingFile.close()
    conclusaoFile.close()


# formata e imprime qualquer matriz (tableau) no arquivo de pivoteamento
def printMatrixP(matrix):
    pivotingFile.write('[')
    for i in range(0, matrix.shape[0]):
        pivotingFile.write('[')

        for j in range(0, matrix.shape[1]):
            pivotingFile.write(np.format_float_positional(float(matrix[i, j]), precision=5))
            #print(float(matrix[i, j]), end='')

            if j != (matrix.shape[1] - 1):
                pivotingFile.write(', ')

        pivotingFile.write(']')
        if i != (matrix.shape[0] - 1):
            pivotingFile.write('\n')
    pivotingFile.write(']' + '\n\n')


# formata e imprime qualquer matriz (vetor) no arquivo de conclusão
def printMatrixC(matrix):
    conclusaoFile.write('[')
    for i in range(0, matrix.shape[0]):
        conclusaoFile.write('[')

        for j in range(0, matrix.shape[1]):
            conclusaoFile.write(np.format_float_positional(float(matrix[i, j]), precision=5))
            # print(float(matrix[i, j]))
            if j != (matrix.shape[1] - 1):
                conclusaoFile.write(', ')

        conclusaoFile.write(']')
        if i != (matrix.shape[0] - 1):
            conclusaoFile.write('\n')
    conclusaoFile.write(']' + '\n')
