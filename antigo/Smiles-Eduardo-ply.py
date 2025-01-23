
from ply.yacc import yacc
from ply.lex import lex
import json
import re

tp = None # tabela periodica

with open("tabela_periodica.json") as tp_arquivo:
    tp = json.load(tp_arquivo)

def gera_regex_de_lista(lista:list[str]) -> str:
    elementos_em_re = []
    for elemento in lista:
        elementos_em_re.append(re.escape(elemento))

    return '|'.join(elementos_em_re)


atomos_organicos = ["H","N","O","P","S","F","Cl","Br","I", "C"] # direto do artigo, tem mais?
atomos_inorganicos = list(set(tp.keys()) - set(atomos_organicos))

t_organico = fr"{gera_regex_de_lista(atomos_organicos)}" # gera as regex
t_inorganico = fr"{gera_regex_de_lista(atomos_inorganicos)}" #gera as regex

def t_numero(t): 
    r'\d+'
    t.value = int(t.value)
    return t

literals =[
    '[',
    ']',
    '=',
    '#',
    '(',
    ')',
    '%',
    '+',
    '-',
    '.',
    ':'
]

tokens = ('organico','inorganico', 'numero')

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    print(f"Caractere inesperado '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex()

# ====================================
def p_mol(regras):
    """
    MOL : SUB_MOL MOL
        | '-' MOL
        | '=' MOL
        | '#' MOL
        | ':' MOL
        | '(' MOL ')' MOL
        | '(' MOL ')' 
        | '%' MOL
        | SUB_MOL
    """
    
    pass

def p_sub_mol(regras):
    """
    SUB_MOL : '[' ELEMENTOS ']'
                   | '[' ELEMENTOS SINAL ']'
                   | ELEMENTOS
    """
    pass

def p_sinal(regras):
    """
    SINAL : '+'
          | '-'
          | '+' SINAL
          | '-' SINAL
    """
    pass

def p_elementos(regras):
    """
    ELEMENTOS : NUM_ELEM ELEMENTOS
              | NUM_ELEM
    """
    pass

def p_num_elem(regras):
    """
    NUM_ELEM : numero ELEMENTO
            | ELEMENTO numero
            | ELEMENTO
    """

def p_ELEMENTO(regras):
    """
    ELEMENTO : organico
            | inorganico
    """
    regras[0] = regras[1]
    
def p_error(regras):
    print("Erro de sintaxe"+ str(regras))

parser = yacc()

while True:
    try:
        s = input('Smiles Mol > ')
    except EOFError:
        break
    if not s:
        continue
    
    if Chem.MolFromSmiles(s):
        result = parser.parse(s)
        print('Here')
        print(result == None)
    else:
        print(False)
    