#1 - Construa uma Gramática e uma Tabela de Símbolos para uma linguagem de programação que respeite
#os seguintes critérios:

#Há somente o tipo de dado número inteiro;

#As variáveis não são tipadas;

#Declaração e atribuição de variáveis deve ser a mesma sintaxe (igual o Python);

#Deve realizar as operações matemáticas básicas (+, -, *, / ) com variáveis e números inteiro,
#respeitando a associatividade e precedência dos operadores;

#Deve permitir expressões matemáticas prioritárias entre parênteses nas operações matemáticas;

#Declaração e atribuição de variável pode haver operações matemática;

#Implementar os blocos condicionais "if" e "else";

#A condição do "if" somente irá comparar 2 valores, podendo ser variável ou números inteiro,
#com os operadores igual, menor, maior e diferente (definir os símbolos para os operadores).

import re

class Lexico:

    token_patterns = [
        ('NUM', r'\d+'),                          # Números inteiros
        ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),        # Identificadores
        ('ASSIGN', r'='),                         # Atribuição
        ('PLUS', r'\+'),                          # Operador +
        ('MINUS', r'-'),                          # Operador -
        ('MUL', r'\*'),                           # Operador *
        ('DIV', r'/'),                            # Operador /
        ('EQ', r'=='),                            # Igualdade ==
        ('NEQ', r'!='),                           # Diferente !=
        ('LT', r'<'),                             # Menor que <
        ('GT', r'>'),                             # Maior que >
        ('LPAREN', r'\('),                        # Parêntese esquerdo
        ('RPAREN', r'\)'),                        # Parêntese direito
        ('IF', r'if'),                            # Palavra reservada 'if'
        ('ELSE', r'else'),                        # Palavra reservada 'else'
        ('LBRACE', r'\{'),                        # Chave esquerda
        ('RBRACE', r'\}'),                        # Chave direita
        ('SEMICOLON', r';'),                      # Ponto e vírgula
        ('WHITESPACE', r'\s+'),                   # Espaços em branco (serão ignorados)
    ]

    def lexico(self, code):
        tokens = []
        index = 0

        while index < len(code):
            match = None
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(code, index)
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE':
                        tokens.append((token_type, value))
                    index = match.end(0)
                    break
            if not match:
                raise ValueError(f"Erro Léxico: Token inválido na posição {index}")
        
        return tokens

Exemplo = """
p = 8;
q = 4;
r = (p + q) * (p - q) / 2;
"""

lexer = Lexico()

tokens = lexer.lexico(Exemplo)

for token in tokens:
    print(token)
