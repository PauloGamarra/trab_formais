import re

class automata:
    def __init__(self, nome, estados, simbolos, inicial, finais, tabela):
        self.nome = nome
        self.estados = estados
        self.simbolos = simbolos
        self.inicial = inicial
        self.finais = finais
        self.tabela = tabela

    def afn_to_afd(self):
        afd = automata(self.nome, [{self.inicial}], self.simbolos, {self.inicial}, [], dict())


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
        atual = transicao.split('=')[0][1:].split(',')[0]
        simbolo = transicao.split('=')[0][1:].split(',')[1][:-1]
        prox = transicao.split('=')[1][:-1]

        tabela[atual][simbolo].append(prox)

    return automata(nome, estados, simbolos,inicial,finais,tabela)

automato = load_fa('./afn_entrada.txt')
automato.afn_to_afd()