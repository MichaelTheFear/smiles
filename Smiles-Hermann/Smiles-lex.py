import ply.lex as lex

tokens = (
    'ATOM',
    'LPAREN',
    'RPAREN',
)

Valencia=dict([('C',4),('N',3),('O',2),('H',1)])
t_LPAREN= r'\('
t_RPAREN = r'\)'

def t_ATOM(t):
    r'[CNOH]'
    print("t.value", t.value)
    print(Valencia[t.value])
    return t

#t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Caractere inválido: '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
