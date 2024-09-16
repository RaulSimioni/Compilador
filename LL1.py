# 2 - Implemente um Analisador Léxico e um Analisador Sintático Preditivo LL(1)
# para a linguagem desenvolvida. 

# O que será avaliado?
# Se a tabela de símbolos e a gramática estão de acordo com os critérios definidos;
# Se o os algoritmos implementam as técnicas apresentadas e especificadas;
# Se o algoritmo analisará corretamente as entradas definidas na hora da avaliação em sala.

import Lexico

class LL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos]

    def consumir(self, tipo):

        if self.token_atual[0] == tipo:
            print(f"Consumindo token: {self.token_atual}")
            self.pos += 1
            if self.pos < len(self.tokens):
                self.token_atual = self.tokens[self.pos]
        else:
            raise ValueError(f"Erro Sintático: esperado {tipo}, mas encontrado {self.token_atual[0]}")

    def parse_programa(self):

        print("Iniciando análise do programa...")
        while self.token_atual[0] in ['ID', 'IF']: 
            self.parse_declaracao()
        print("Análise do programa concluída.")

    def parse_declaracao(self):

        if self.token_atual[0] == 'ID':
            self.parse_atribuicao()
        elif self.token_atual[0] == 'IF':
            self.parse_condicional()
        else:
            raise ValueError(f"Erro Sintático: Declaração inválida na posição {self.pos}")

    def parse_atribuicao(self):

        print("Analisando atribuição...")
        self.consumir('ID')      
        self.consumir('ASSIGN')
        self.parse_expressao()    
        self.consumir('SEMICOLON')

    def parse_condicional(self):

        print("Analisando condicional...")
        self.consumir('IF')
        self.consumir('LPAREN')
        self.parse_condicao()
        self.consumir('RPAREN')
        self.consumir('LBRACE')
        self.parse_bloco()
        self.consumir('RBRACE')

        if self.token_atual[0] == 'ELSE':
            self.consumir('ELSE')
            self.consumir('LBRACE')
            self.parse_bloco()
            self.consumir('RBRACE')

    def parse_bloco(self):

        print("Analisando bloco...")
        while self.token_atual[0] in ['ID', 'IF']:
            self.parse_declaracao()

    def parse_condicao(self):

        print("Analisando condição...")
        self.parse_expressao()
        if self.token_atual[0] in ['EQ', 'NEQ', 'LT', 'GT']:
            self.consumir(self.token_atual[0])
        else:
            raise ValueError(f"Erro Sintático: Operador relacional inválido encontrado na posição {self.pos}")
        self.parse_expressao()

    def parse_expressao(self):

        print("Analisando expressão...")
        self.parse_termo()
        while self.token_atual[0] in ['PLUS', 'MINUS']:
            self.consumir(self.token_atual[0])
            self.parse_termo()

    def parse_termo(self):

        print("Analisando termo...")
        self.parse_fator()
        while self.token_atual[0] in ['MUL', 'DIV']:
            self.consumir(self.token_atual[0])
            self.parse_fator()

    def parse_fator(self):

        print("Analisando fator...")
        if self.token_atual[0] == 'NUM':
            self.consumir('NUM')
        elif self.token_atual[0] == 'ID':
            self.consumir('ID')
        elif self.token_atual[0] == 'LPAREN':
            self.consumir('LPAREN')
            self.parse_expressao()  
            self.consumir('RPAREN')  
        else:
            raise ValueError(f"Erro Sintático: Fator inválido encontrado na posição {self.pos}")

Exemplo = """
p = 8;
q = 4;
r = (p + q) * (p - q) / 2;
"""

lexer = Lexico.lexer

tokens = lexer.lexico(Exemplo)

parser = LL1(tokens)
parser.parse_programa()