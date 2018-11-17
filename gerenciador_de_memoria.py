class Node:
    def __init__(self, tipo, numero):
        self.tipo = tipo # se representa um bloco livre ou ocupado
        self.numero = numero # pra identificar o bloco
        self.inicio = 0 # inicio do bloco
        self.fim = 0 # fim do bloco
        self.anterior = None # o bloco anterior
        self.proximo = None# o proximo bloco

class List:
    def __init__(self, maximo, minimo):
        nodo = Node('L', 0)
        nodo.inicio = minimo
        nodo.fim = maximo
        self.head = nodo # o primeiro bloco
        self.tail = nodo# o ultimo bloco
        self.max = maximo # o valor maximo do espaco de memoria
        self.min = minimo # o valor minimo do espaco de memoria
        self.waiting_list = [] # lista para os blocos em que ocorreu fragmentacao externa

    def add_Bloco(self,aux, nodo, quant):
        if aux.tipo == 'L' and (aux.fim - aux.inicio) > quant:
            # nao importa se for o ultimo pq o ultimo continua existindo com o espaco que sobrar nele
            if aux == self.head: # se for o primeiro nodo
                nodo.inicio = aux.inicio
                aux.inicio = aux.inicio + quant
                nodo.fim = aux.inicio
                aux.anterior = nodo
                nodo.proximo = aux
                self.head = nodo
                print("Alocacao realizada para o Bloco ",nodo.numero," na regiao ",nodo.inicio,"-",nodo.fim)
                return True
            else: # pra qualquer nodo no meio ou no fim da lista
                nodo.inicio = aux.inicio
                aux.inicio = aux.inicio + quant
                nodo.fim = aux.inicio
                nodo.anterior = aux.anterior
                aux.anterior.proximo = nodo
                aux.anterior = nodo
                nodo.proximo = aux
                print("Alocacao realizada para o Bloco ",nodo.numero," na regiao ",nodo.inicio,"-",nodo.fim)
                return True
        elif aux.tipo == 'L' and (aux.fim - aux.inicio) == quant:
                aux.numero = nodo.numero
                aux.tipo = 'S'
                print("Alocacao realizada para o Bloco ",aux.numero," na regiao ",aux.inicio,"-",aux.fim)
                return True

        elif aux == self.tail:
            if not ((nodo,quant) in self.waiting_list):
                self.waiting_list.append((nodo,quant))
            self.fragmentacao(self.head, quant, 0)
            return False
        else:
            return self.add_Bloco(aux.proximo, nodo, quant)

    def fragmentacao(self, aux, quant, livre):
        if aux.tipo == "S":
            print(aux.inicio,"-",aux.fim,"  bloco ",aux.numero," (tamanho ",aux.fim-aux.inicio,")")
        else:
            livre += (aux.fim-aux.inicio)
            print(aux.inicio,"-",aux.fim,"  livre (tamanho ",aux.fim-aux.inicio,")")
        if aux == self.tail:
            print(livre," livres, ",quant," solicitados - fragmentacao externa")
        else:
            self.fragmentacao(aux.proximo, quant, livre)

    def reorganize(self, aux):
        if aux != self.tail:
            while aux.proximo.tipo == 'L':
                removido = aux.proximo
                aux.fim = removido.fim
                aux.proximo = removido.proximo
                if removido == self.tail:
                    self.tail = aux
                    break
                removido.proximo.anterior = aux

        if aux != self.head:
            while aux.anterior.tipo == 'L':
                removido = aux.anterior
                aux.inicio = removido.inicio
                aux.anterior = removido.anterior
                if removido == self.head:
                    self.head = aux
                    break
                removido.anterior.proximo = aux

    def free_Bloco(self, aux,  numero):
        if aux.tipo == 'S' and aux.numero == numero:
            aux.tipo = 'L'
            aux.numero = 0
            inicio = aux.inicio
            fim = aux.fim
            self.reorganize(aux)
            print("Bloco ",numero," (",inicio,"-",fim,") liberado com sucesso")
            self.search_space()
        elif aux == self.tail:
            print("Nenhum bloco com este numero encontrado.")
        else:
            self.free_Bloco(aux.proximo, numero)

    def search_space(self):
        removido_index = None
        res = False
        for i in range(0,len(self.waiting_list)):
            nodo, quant = self.waiting_list[i]
            res = self.add_Bloco(self.head, nodo, quant)
            if res:
                removido_index = i
                break
        if res:
            del self.waiting_list[removido_index]
            self.search_space()



with open('casoTeste1.txt', 'r') as file:
    indexBlocos = 1
    line = file.readline()
    modo = int(line)
    line = file.readline()
    mi = int(line)
    line = file.readline()
    mf = int(line)
    lista = List(mf, mi)
    for line in file:
        tipo, num = line.split(' ')
        num = int(num)
        if tipo == "S":
            nodo = Node(tipo,indexBlocos)
            lista.add_Bloco(lista.head, nodo, num)
            indexBlocos = indexBlocos + 1
        elif tipo == "L":
            lista.free_Bloco(lista.head,num)
