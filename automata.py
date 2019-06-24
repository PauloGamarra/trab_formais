import os

class automata:
    def __init__(self, nome, estados, simbolos, inicial, finais, tabela):
        self.nome = nome
        self.estados = estados
        self.simbolos = simbolos
        self.inicial = inicial
        self.finais = finais
        self.tabela = tabela

    def afn_to_afd(self):
        afd = automata(self.nome, [], self.simbolos, self.inicial, [], dict())

        novos_estados = set([frozenset([afd.inicial])]) #inicia a fila de novos estados compostos apenas com o inicial
        tabela = dict()

        while novos_estados: #enquanto a fila de estados não estiver vazia
            estado_composto = novos_estados.pop()
            tabela.update(dict({estado_composto:dict(zip([simbolo for simbolo in afd.simbolos], [[] for simbolo in afd.simbolos]))}))
            afd.estados.append(estado_composto)
            for simbolo in afd.simbolos:

                alcancaveis = set()

                for estado in estado_composto:
                    alcancaveis.update(self.tabela[estado][simbolo])

                tabela[estado_composto][simbolo] = alcancaveis

                if alcancaveis not in afd.estados and alcancaveis != frozenset():
                    novos_estados.add(frozenset(alcancaveis))

            for final in self.finais:
                if final in estado_composto:
                    afd.finais.append(str(list(estado_composto))[1:-1].replace("'","").replace(", ","|")) #q1|q1|q3

        for estado in afd.estados:
            afd.tabela[str(list(estado))[1:-1].replace("'","").replace(", ","|")] = dict(zip([simbolo for simbolo in afd.simbolos], [[] for simbolo in afd.simbolos]))
            for simbolo in afd.simbolos:
                if tabela[estado][simbolo] != set({}):
                    afd.tabela[str(list(estado))[1:-1].replace("'","").replace(", ","|")][simbolo] = str(tabela[estado][simbolo])[1:-1].replace("'","").replace(", ","|")
                else:
                    afd.tabela[str(list(estado))[1:-1].replace("'","").replace(", ","|")][simbolo] = None
            afd.estados[afd.estados.index(estado)] = str(list(estado))[1:-1].replace("'","").replace(", ","|")

        afd.nome = self.nome + '_D'

        with open(afd.nome+'.txt', 'w') as afd_saida:
            afd_saida.write(afd.nome+'=('+str(afd.estados).replace(' ','').replace('[','{').replace(']','}').replace("'",'')+','+str(afd.simbolos).replace('[','{').replace(']','}').replace(' ','').replace("'",'')+','+afd.inicial+','+str(afd.finais).replace(' ','').replace('[','{').replace(']','}').replace("'",'')+')')
            afd_saida.write('\nProg')
            for transicao in afd.tabela:
                for simbolo in afd.simbolos:
                    if afd.tabela[transicao][simbolo] != None:
                        afd_saida.write('\n('+transicao+','+simbolo+')='+afd.tabela[transicao][simbolo])


        return afd

    def test_input(self, palavra):
        palavra = palavra.split('|')
        estado = self.inicial
        for simbolo in palavra:
            if self.tabela[estado][simbolo] != None:
                estado = self.tabela[estado][simbolo]
            else:
                return False
        if estado in self.finais:
            return True
        else:
            return False


def load_fa(path):
    with open(path,'r') as file:
        lines = file.readlines()

    nome = lines[0].split('=')[0]
    estados = lines[0].split('=')[1].split('}')[0][2:].split(',')
    simbolos = lines[0].split('=')[1].split('}')[1][2:].split(',')
    inicial = lines[0].split('=')[1].split('}')[2].split(',')[1]
    finais = lines[0].split('=')[1].split('}')[2].split('{')[1].split(',')

    tabela = dict(zip([estado for estado in estados], [[] for estado in estados]))
    for estado in tabela:
        tabela[estado] = dict(zip([simbolo for simbolo in simbolos], [[] for simbolo in simbolos]))

    for transicao in lines[2:]:
        if transicao:
            atual = transicao.split('=')[0][1:].split(',')[0]
            simbolo = transicao.split('=')[0][1:].split(',')[1][:-1]
            prox = transicao.split('=')[1].replace("\n","")

        tabela[atual][simbolo].append(prox)

    return automata(nome, estados, simbolos, inicial, finais, tabela)

def main():

    while(True):

        os.system('cls' if os.name == 'nt' else 'clear')
        arq_automato = input("Arquivo do automato de entrada (enter para encerrar): ")

        if os.path.isfile(arq_automato): #se o usuário escreveu um arquivo válido, a leitura como automato é feita

            automato = load_fa(arq_automato)
            os.system('cls' if os.name == 'nt' else 'clear')
            automato = automato.afn_to_afd()

            if input('Automato carregado e convertido para afd com sucesso. Imprimir transicoes?[S,n] ').lower() == 's':
                #se o usuário aceitar, em cada linha são impressas as transicoes de um estado
                os.system('cls' if os.name == 'nt' else 'clear')
                for transicao in automato.tabela:
                    print(transicao, automato.tabela[transicao])
                input("Pressione enter para continuar...")

            while(True):

                os.system('cls' if os.name == 'nt' else 'clear')
                arq_palavras = input("Arquivo com as palavras a serem testadas: ")

                #se o arquivo existir, é aberto para leitura
                if os.path.isfile(arq_palavras):

                    with open(arq_palavras, 'r') as file:

                        for palavra in file.readlines():
                            print(palavra.replace('\n',''), ': ' , end='')
                            if automato.test_input(palavra.replace('\n','')):
                                print('Aceita({})'.format(automato.nome))
                            else:
                                print('Rejeita({})'.format(automato.nome))
                        input("Pressione enter para continuar...")

                #se não, o usuario pode tentar de novo ou encerrar a leitura
                else:

                    os.system('cls' if os.name == 'nt' else 'clear')
                    if input("Arquivo inexistente. Encerrar leitura?[S,n] ").lower() == 's':
                        break

        else: #caso o arquivo não exista
            if arq_automato: #se foi escrito alguma coisa, o usuário se enganou

                os.system('cls' if os.name == 'nt' else 'clear')
                if input("Arquivo inexistente. Encerrar programa?[S,n] ").lower() == 's':
                    break

            else: #se não o usuário pediu para encerrar o programa apenas clicando enter

                break


if __name__ == '__main__':
    main()