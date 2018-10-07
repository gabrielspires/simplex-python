from utils import printConclusao
from utils import printPivoting
from fractions import Fraction
from matrix import Matrix
import numpy as np

# facilita a seleção das opções
NONVIABLE = 0
UNBOUNDED = 1
LIMITED = 2


# classe que mantém todos os métodos do simplex agrupados
class Simplex:
    # instância da PL que será usada
    matrix = Matrix()
    # flag que indica se a PL é a original ou a auxiliar
    auxiliary = False

    # prepara para iniciar o programa
    def init(self, m, r, c):
        self.matrix.init(m, r, c)
        self.matrix.tableau()
        # self.selection()
        
        

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

    # testa se a PL possui um caso de invialibilidade
    # caso: linha de A toda positiva, mas b correspondente é negativo
    # obs: é testado só quando há dual pois b tem que ter ao menos um negativo
    def testNonViable(self):
        for i in range(1, self.matrix.getB().shape[0]):
            # flag de validade: começa considerando a linha correspondente ao b negativo como inválida. Se achar pelo menos um elemento negativo na matriz A, a linha passa a ser válida
            valid = False
            # procura b negativo
            if(self.matrix.getB()[i, 0] < 0):
                # variável para guardar qual a linha problemática
                index = i
                for j in range(0, self.matrix.getA().shape[1]):
                    # procura A negativo na linha b
                    if(self.matrix.getA()[i - 1, j] < 0):
                        valid = True
                        break
                # se passou pela linha do A inteira e não achou ninguém negativo, a PL é inviável e essa linha é problemática
                if(valid is False):
                    return (index, False)
        # caso não tenha entrado no critério para nenhuma das linhas, retorna uma linha não existente e confirma viabilidade da PL
        return (-1, True)

    # testa se a PL possui um caso de ilimitabilidade
    # caso: coluna (considerando -c) composta por 0s ou valores negativos
    # obs: é testado só quando há primal em PL original
    def testUnbounded(self):
        for i in range(0, self.matrix.getC().shape[1]):
            # flag de validade: começa considerando a coluna correspondente ao -c negativo como inválida. Se achar pelo menos um elemento positivo na matriz A, a linha passa a ser válida
            valid = False
            # procura -c negativo
            if(self.matrix.getC()[0, i] < 0):
                # guarda coluna problemática
                index = i
                for j in range(0, self.matrix.getA().shape[0]):
                    # procura por A positivo na coluna
                    if(self.matrix.getA()[j, i] > 0):
                        valid = True
                        break
                # se passou pela coluna do A inteira e não achou ninguém positivo, a PL é ilimitada e essa coluna é problemática
                if(valid is False):
                    return (index, False)
        # caso não tenha entrado no critério, retorna uma coluna não existente e confirma limitabilidade da PL
        return (-1, True)

    # se confirmado caso de invialibilidade (tanto na PL auxiliar como no dual simplex), esta função que trata o caso e extrai o certificado
    def nonViable(self, rIndex=None):
        if(self.auxiliary is True):
            # se o problema é na PL auxiliar, extrai seu certificado de otimalidade (que é o de invialibilidade da PL original)
            printConclusao(NONVIABLE, self.matrix.getMem()[0])
        else:
            # se o problema é no dual simplex, extrai a linha da matriz de registros referente à linha problemática
            printConclusao(NONVIABLE, self.matrix.getMem()[rIndex])

    # se confirmado caso de PL ilimitada, trata o caso e monta o certificado
    def unbounded(self, cIndex=None):
        certificate = np.zeros((1, self.matrix.getA().shape[1]), dtype='object')
        # fixa 1 na coluna do certificado correspondente à coluna problemática
        certificate[0, cIndex] = 1

        for i in range(0, self.matrix.getA().shape[1]):
            for j in self.matrix.base:
                # para cada coluna de A, confere se ela é da base de soluções
                if((self.matrix.getMem().shape[1] + i) == j[1]):
                    # coloca o inverso do valor naquela linha da coluna problemática
                    certificate[0, i] = -1 * self.matrix.getA()[j[0] - 1, cIndex]

        # envia certificado para função que imprimi no arquivo de saída
        printConclusao(UNBOUNDED, certificate)

    # se confirmado caso de otimalidade, extrai certificado, valor objetivo e solução correspondentes à PL
    def end(self):
        solution = self.getSolution()
        printConclusao(LIMITED, self.matrix.getMem()[0], self.matrix.getB()[0, 0], solution)

    # escolhe elemento pivô para um passo do simplex primal
    def primalPivot(self):
        rIndex = -1
        cIndex = -1

        # procura -c negativo
        for i in range(0, self.matrix.getC().shape[1]):
            if(self.matrix.getC()[0, i] < 0):
                cIndex = i
                break

        # float('inf') só pega maior valor possível para iniciar a escolha
        ratio = float('inf')
        for i in range(0, self.matrix.getA().shape[0]):
            if(self.matrix.getA()[i, cIndex] > 0):
                # calcula a razão entre o A positivo na coluna do -c escolhido e o b da linha correspondente ao A
                aux = Fraction(self.matrix.getB()[i + 1, 0], self.matrix.getA()[i, cIndex])
                # confere se a razão achada é a menor até o momento e atualiza posição do pivô atual
                if(aux < ratio):
                    ratio = aux
                    rIndex = i

        # retorna posição do pivô em relação ao tableau inteiro
        return (self.matrix.getC().shape[0] + rIndex, self.matrix.getMem().shape[1] + cIndex)

    # aplica uma etapa do primal simplex
    def primal(self):
        # acha posição do pivô
        (row, col) = self.primalPivot()
        # pivoteia naquela posição
        self.matrix.pivoting(row, col)
        # imprime no arquivo o tableau pivoteado
        printPivoting(self.matrix.tableau)
        # volta à função de seleção
        self.selection()

    # escolhe elemento pivÔ para um passo do simplex dual
    def dualPivot(self):
        rIndex = -1
        cIndex = -1

        # procura b negativo
        for i in range(1, self.matrix.getB().shape[0]):
            if(self.matrix.getB()[i, 0] < 0):
                rIndex = i - 1
                break

        ratio = float('inf')
        for i in range(0, self.matrix.getA().shape[1]):
            if(self.matrix.getA()[rIndex, i] < 0):
                # calcula a razão (em valor absoluto) entre o A negativo na linha do b escolhido e o -c da coluna correspondente ao A
                aux = abs(Fraction(self.matrix.getC()[0, i], self.matrix.getA()[rIndex, i]))
                if(aux < ratio):
                    ratio = aux
                    cIndex = i

        # retorna posição do pivô em relação ao tableau inteiro
        return(self.matrix.getC().shape[0] + rIndex, self.matrix.getMem().shape[1] + cIndex)

    # aplica uma etapa do simplex dual
    def dual(self):
        # acha posição do pivô
        (row, col) = self.dualPivot()
        # pivoteia naquela posição
        self.matrix.pivoting(row, col)
        # imprime no arquivo o tableau pivoteado
        printPivoting(self.matrix.tableau)
        # volta à função de seleção
        self.selection()

    # ajusta a PL para obter a PL auxiliar
    def adjustMatrix(self):
        # multiplica entradas negativas do b por -1
        for i in range(1, self.matrix.getB().shape[0]):
            if(self.matrix.getB()[i, 0] < 0):
                self.matrix.tableau[i, :] = -1 * self.matrix.tableau[i, :]

        # monta a PL auxiliar
        self.matrix.extendAuxiliary()

        # pivoteia as bases para torná-las ótimas
        for i in range(0, len(self.matrix.base)):
            self.matrix.pivoting(self.matrix.base[i][0], self.matrix.base[i][1])

        # faz simplex para PL auxiliar
        self.selection()

    # avalia resultado da PL auxiliar
    def evalAuxiliary(self):
        # caso 1: valor objetivo da PL auxiliar é 0 --> PL original é viável
        if(self.matrix.getB()[0, 0] == 0):
            # volta para a PL original
            self.matrix.destroyAuxiliary()
            self.auxiliary = False

            # restaura bases encontradas com a PL auxiliar
            for i in range(0, len(self.matrix.base)):
                self.matrix.pivoting(self.matrix.base[i][0], self.matrix.base[i][1])

            # faz simplex para PL original
            self.selection()
        # caso 2: valor objetivo da PL auxiliar é < 0 --> PL original é inviável
        elif(self.matrix.getB()[0, 0] < 0):
            self.nonViable()

    # monta vetor de soluções para a base de soluções da PL ótima
    def getSolution(self):
        solution = np.zeros((1, self.matrix.c.shape[1]), dtype='object')

        for i in range(0, (self.matrix.getA().shape[1] - self.matrix.getGap().shape[1])):
            for j in self.matrix.base:
                # confere se coluna está na base
                if((self.matrix.getMem().shape[1] + i) == j[1]):
                    # pega b correspondente à solução naquela coluna
                    solution[0, i] = self.matrix.getB()[j[0], 0]

        return solution
