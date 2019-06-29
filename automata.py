import os


class automata:
    def __init__(self, nome, estados, simbolos, inicial, finais, tabela):
        self.nome = nome  # string
        self.estados = estados  # lista de strings
        self.simbolos = simbolos  # lista de strings
        self.inicial = inicial  # string
        self.finais = finais  # lista de strings
        self.tabela = tabela  # dicionário de strings(estado) para dicionário de strings(simbolo) para strings(estado). Ex self.tabela['q1']['a'] = ['q2']

    def afn_to_afd(self):
        afd = automata(self.nome, [], self.simbolos, self.inicial, [], dict())

        novos_estados = set(
            [frozenset([afd.inicial])])  # inicia o conjunto de novos estados compostos apenas com o inicial
        # um estado composto é um conjunto de strings que representam estados
        tabela = dict()  # inicia a nova tabela de transição de estados

        while novos_estados:  # enquanto a fila de estados não estiver vazia
            estado_composto = novos_estados.pop()  # retira um estado composto aleatŕorio do conjunto de estados compostos ainda não avaliados
            tabela.update(dict({estado_composto: dict(zip([simbolo for simbolo in afd.simbolos], [[] for simbolo in
                                                                                                  afd.simbolos]))}))  # cria uma coluna na tabela para o novo estado composto
            afd.estados.append(estado_composto)  # e insere o novo estado composto na lista de estados do afd
            for simbolo in afd.simbolos:
                # para cada símbolo, testa quais outros estados podem ser alcançados pelo estado composto
                alcancaveis = set()

                for estado in estado_composto:
                    # cada novo estado possivel de ser alcancado pelo estado composto é adicionado no conjunto de alcancaveis
                    alcancaveis.update(self.tabela[estado][simbolo])

                # quando todos os alcancaveis são computados para um simbolo, ele é inserido como o estado composto resultante de uma transicao com esse simbolo
                tabela[estado_composto][simbolo] = alcancaveis

                # se o estado composto dos alcancaveis ainda nao estiver na lista de estados e nao for um conjunto vazio, ele é adicionado
                if alcancaveis not in afd.estados and alcancaveis != frozenset():
                    novos_estados.add(frozenset(alcancaveis))

            # se esse novo estado comosto possuir um estado final do afn, ele é adicioando À lista de estados finais do afd na forma de uma string '<estado0>|<estado1>|...|<estadoN>'
            for final in self.finais:
                if final in estado_composto:
                    afd.finais.append(str(list(estado_composto))[1:-1].replace("'", "").replace(", ", "|"))  # q1|q1|q3

        # quando a tabela do afn já for computada, ela é formatada para que os estados compostos sejam strings da forma '<estado0>|<estado1>|...|<estadoN>' ao invés de conjuntos
        for estado in afd.estados:
            afd.tabela[str(list(estado))[1:-1].replace("'", "").replace(", ", "|")] = dict(
                zip([simbolo for simbolo in afd.simbolos], [[] for simbolo in afd.simbolos]))
            for simbolo in afd.simbolos:
                if tabela[estado][simbolo] != set({}):
                    afd.tabela[str(list(estado))[1:-1].replace("'", "").replace(", ", "|")][simbolo] = str(
                        tabela[estado][simbolo])[1:-1].replace("'", "").replace(", ", "|")
                else:
                    afd.tabela[str(list(estado))[1:-1].replace("'", "").replace(", ", "|")][simbolo] = None
            afd.estados[afd.estados.index(estado)] = str(list(estado))[1:-1].replace("'", "").replace(", ", "|")

        afd.nome = self.nome + '_D'

        # por fim o AFD é escrito no arquivo de saida
        with open(afd.nome + '.txt', 'w') as afd_saida:
            afd_saida.write(
                afd.nome + '=(' + str(afd.estados).replace(' ', '').replace('[', '{').replace(']', '}').replace("'",
                                                                                                                '') + ',' + str(
                    afd.simbolos).replace('[', '{').replace(']', '}').replace(' ', '').replace("'",
                                                                                               '') + ',' + afd.inicial + ',' + str(
                    afd.finais).replace(' ', '').replace('[', '{').replace(']', '}').replace("'", '') + ')')
            afd_saida.write('\nProg')
            for transicao in afd.tabela:
                for simbolo in afd.simbolos:
                    if afd.tabela[transicao][simbolo] != None:
                        afd_saida.write('\n(' + transicao + ',' + simbolo + ')=' + afd.tabela[transicao][simbolo])

        return afd

    def test_input(self, palavra):
        palavra = palavra.split('|')  # palavra é uma lista com a sequencia de símbolos da palavra
        estado = self.inicial
        for simbolo in palavra:  # para cada simbolo é feita uma transicao no automato
            if self.tabela[estado][simbolo] != None:
                estado = self.tabela[estado][simbolo]
            else:
                return False  # se houver uma indeterminação a palavra é rejeitada
        if estado in self.finais:  # se no o ultimo estado alcançado for final, a palavra é aceita
            return True
        else:  # se não, é rejeitada
            return False


def load_fa(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    # separa todas as informações contidas na primeira linha do arquivo
    nome = lines[0].split('=')[0]
    estados = lines[0].split('=')[1].split('}')[0][2:].split(',')
    simbolos = lines[0].split('=')[1].split('}')[1][2:].split(',')
    inicial = lines[0].split('=')[1].split('}')[2].split(',')[1]
    finais = lines[0].split('=')[1].split('}')[2].split('{')[1].split(',')

    # cria a tabela de transicoes com as ainda vazias
    tabela = dict(zip([estado for estado in estados], [[] for estado in estados]))
    for estado in tabela:
        tabela[estado] = dict(zip([simbolo for simbolo in simbolos], [[] for simbolo in simbolos]))

    # le cada linha a partir da terceira e atualiza a tabela com as transicoes
    for transicao in lines[2:]:
        if transicao:
            atual = transicao.split('=')[0][1:].split(',')[0]
            simbolo = transicao.split('=')[0][1:].split(',')[1][:-1]
            prox = transicao.split('=')[1].replace("\n", "")

        tabela[atual][simbolo].append(prox)

    # retorna o automato inicializado
    return automata(nome, estados, simbolos, inicial, finais, tabela)


def main():
    while (True):

        os.system('cls' if os.name == 'nt' else 'clear')  # limpa tela
        arq_automato = input("Arquivo do automato de entrada (enter para encerrar): ")

        if os.path.isfile(arq_automato):  # se o usuário escreveu um arquivo válido, a leitura como automato é feita

            automato = load_fa(arq_automato)  # é carregado o automato
            os.system('cls' if os.name == 'nt' else 'clear')
            automato = automato.afn_to_afd()  # o automato é convertido para afd

            if input('Automato carregado e convertido para afd com sucesso. Imprimir transicoes?[S,n] ').lower() == 's':
                # se o usuário aceitar, em cada linha são impressas as transicoes de um estado
                os.system('cls' if os.name == 'nt' else 'clear')
                for transicao in automato.tabela:
                    print(transicao, automato.tabela[transicao])
                input("Pressione enter para continuar...")

            while (True):

                os.system('cls' if os.name == 'nt' else 'clear')
                arq_palavras = input("Arquivo com as palavras a serem testadas: ")

                # se o arquivo existir, é aberto para leitura
                if os.path.isfile(arq_palavras):

                    with open(arq_palavras, 'r') as file:
                        # para cada linha contendo uma palavra do arquivo, essa palavra é testada e é impresso se o automato aceita ou rejeita
                        for palavra in file.readlines():
                            print(palavra.replace('\n', ''), ': ', end='')
                            if automato.test_input(palavra.replace('\n', '')):
                                print('Aceita({})'.format(automato.nome))
                            else:
                                print('Rejeita({})'.format(automato.nome))
                        input("Pressione enter para continuar...")

                # se não, o usuario pode tentar de novo ou encerrar a leitura
                else:

                    os.system('cls' if os.name == 'nt' else 'clear')
                    if input("Arquivo inexistente. Encerrar leitura?[S,n] ").lower() == 's':
                        break

        else:  # caso o arquivo não exista
            if arq_automato:  # se foi escrito alguma coisa, o usuário se enganou

                os.system('cls' if os.name == 'nt' else 'clear')
                if input("Arquivo inexistente. Encerrar programa?[S,n] ").lower() == 's':
                    break

            else:  # se não o usuário pediu para encerrar o programa apenas clicando enter

                break


if __name__ == '__main__':
    main()