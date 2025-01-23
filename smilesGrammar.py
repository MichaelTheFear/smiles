import ply.lex as lex
import ply.yacc as yacc
import re

tokens = ['semi_bond','semi_symbol', 'digit', 'organic_symbol']

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

literals = [".","@","-","+",":","%","H",")","(","]","[", 'H']

bonds = ["=", "#", "$", "/", "\\"]

t_organic_symbol = rf'{gera_regex_de_lista(atomos_organicos)}'
t_semi_symbol = rf'{gera_regex_de_lista(atomos_inorganicos)}'
t_semi_bond = rf'{gera_regex_de_lista(bonds)}'
t_digit = r'\d'


def t_error(t):
    print(f"Caractere inesperado '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()


def p_line(p):
    """
    line : atom 
        | atom chain_branch
    """
    pass

def p_chain_branch(p):
    """
    chain_branch : chains
                | branch
                | chains chain_branch
                | branch chain_branch
    """
    pass

def p_chains(p):
    """
    chains : chain
           | chain chains
    """
    pass

def p_chain(p):
    """
    chain : '.' atom
          | opt_bond atom
          | opt_bond rnum
    """
    pass


def p_branch(p):
    """
    branch : '(' inner_branch ')'
    """
    pass

def p_inner_branch(p):
    """
    inner_branch : opt_bond_dot line
                | opt_bond_dot line inner_branch
    """
    pass

def p_opt_bond(p):
    """
    opt_bond : bond
            | empty
    """
    pass

def p_opt_isotope(p):
    """
    opt_isotope : isotope
                | empty
    """
    pass

def p_opt_chiral(p):
    """
    opt_chiral : chiral
               | empty
    """
    pass

def p_opt_hcount(p):
    """
    opt_hcount : hcount
               | empty
    """
    pass

def p_opt_bond_dot(p):
    """
    opt_bond_dot : bond 
                | '.'
                | empty
    """
    pass

def p_opt_charge(p):
    """
    opt_charge : charge
               | empty
    """

def p_opt_map(p):
    """
    opt_map : map
            | empty
    """
    
def p_opt_digit(p):
    """
    opt_digit : digit
              | empty
    """

def p_bond(p):
    """
    bond : semi_bond
         | '-'
    """
    p[0] = p[1]

def p_semi_symbols(p):
    """
    symbol : semi_symbol
            | 'H'
    """
    
    p[0] = p[1]

def p_atom(p):
    """
    atom : organic_symbol
        | bracket_atom
    """
    
    p[0] = p[1]

def p_bracket_atom(p):
    """
    bracket_atom : '[' opt_isotope symbol opt_chiral opt_hcount opt_charge opt_map ']'
    """
    
    pass

def p_rnum(p):
    """
    rnum : digit
        | '%' digit digit
    """
    pass
    
def p_isotope(p):
    """
    isotope : opt_digit opt_digit digit
    """
    pass

def p_hcount(p):
    """
    hcount : 'H' opt_digit
    """
    pass

def p_charge(p):
    """
    charge : '+'
           | '+' '+'
           | '+' fifteen
           | '-' 
           | '-' '-'
           | '-' fifteen
    """
    pass

def p_map(p):
    """
    map : ':' opt_digit opt_digit digit
    """
    pass

def p_chiral(p):
    """
    chiral : '@'
           | '@' '@'
    """
    pass

def p_fifteen(p):
    """
    fifteen : digit
            | digit digit
    """
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(regras):
    print("Erro de sintaxe"+ str(regras))

parser = yacc.yacc(debug=True)
parser.parse("Br(Cl)")
