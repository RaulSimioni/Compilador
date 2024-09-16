import Lexico

class LL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos]

    def consumir(self, tipo):
        """
        Consome o token atual se ele for do tipo esperado, e move para o próximo token.
        Caso contrário, lança um erro sintático.
        """
        if self.token_atual[0] == tipo:
            print(f"Consumindo token: {self.token_atual}")
            self.pos += 1
            if self.pos < len(self.tokens):
                self.token_atual = self.tokens[self.pos]
        else:
            raise ValueError(f"Erro Sintático: esperado {tipo}, mas encontrado {self.token_atual[0]}")

    def parse_programa(self):
        """
        <programa> ::= <declaração> | <declaração> <programa>
        """
        print("Iniciando análise do programa...")
        while self.token_atual[0] in ['ID', 'IF']:  # Enquanto houver uma declaração
            self.parse_declaracao()
        print("Análise do programa concluída.")

    def parse_declaracao(self):
        """
        <declaração> ::= <atribuição> | <condicional>
        """
        if self.token_atual[0] == 'ID':
            self.parse_atribuicao()
        elif self.token_atual[0] == 'IF':
            self.parse_condicional()
        else:
            raise ValueError(f"Erro Sintático: Declaração inválida na posição {self.pos}")

    def parse_atribuicao(self):
        """
        <atribuição> ::= <id> "=" <expressao> ";"
        """
        print("Analisando atribuição...")
        self.consumir('ID')        # Consome o identificador
        self.consumir('ASSIGN')    # Consome o '='
        self.parse_expressao()     # Analisa a expressão
        self.consumir('SEMICOLON') # Consome o ';'

    def parse_condicional(self):
        """
        <condicional> ::= "if" "(" <condicao> ")" "{" <bloco> "}" ["else" "{" <bloco> "}"]
        """
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
        """
        <bloco> ::= <declaração> | <declaração> <bloco>
        """
        print("Analisando bloco...")
        while self.token_atual[0] in ['ID', 'IF']:
            self.parse_declaracao()

    def parse_condicao(self):
        """
        <condicao> ::= <expressao> <operador_relacional> <expressao>
        """
        print("Analisando condição...")
        self.parse_expressao()
        if self.token_atual[0] in ['EQ', 'NEQ', 'LT', 'GT']:
            self.consumir(self.token_atual[0])  # Consome o operador relacional
        else:
            raise ValueError(f"Erro Sintático: Operador relacional inválido encontrado na posição {self.pos}")
        self.parse_expressao()

    def parse_expressao(self):
        """
        <expressao> ::= <termo> | <termo> <operador_aditivo> <expressao>
        """
        print("Analisando expressão...")
        self.parse_termo()
        while self.token_atual[0] in ['PLUS', 'MINUS']:
            self.consumir(self.token_atual[0])  # Consome o operador + ou -
            self.parse_termo()

    def parse_termo(self):
        """
        <termo> ::= <fator> | <fator> <operador_multiplicativo> <termo>
        """
        print("Analisando termo...")
        self.parse_fator()
        while self.token_atual[0] in ['MUL', 'DIV']:
            self.consumir(self.token_atual[0])  # Consome o operador * ou /
            self.parse_fator()

    def parse_fator(self):
        """
        <fator> ::= <numero> | <id> | "(" <expressao> ")"
        """
        print("Analisando fator...")
        if self.token_atual[0] == 'NUM':
            self.consumir('NUM')  # Consome um número
        elif self.token_atual[0] == 'ID':
            self.consumir('ID')   # Consome um identificador
        elif self.token_atual[0] == 'LPAREN':
            self.consumir('LPAREN')  # Consome '('
            self.parse_expressao()   # Analisa a expressão dentro dos parênteses
            self.consumir('RPAREN')  # Consome ')'
        else:
            raise ValueError(f"Erro Sintático: Fator inválido encontrado na posição {self.pos}")


# Exemplo de código
code_example = """
p = 8;
q = 4;
r = (p + q) * (p - q) / 2;
"""

# Criando uma instância do Lexer
lexer = Lexico.lexer

# Gerando tokens a partir do código fonte
tokens = lexer.lexer(code_example)

# Executando o parser LL(1)
parser = LL1(tokens)
parser.parse_programa()
