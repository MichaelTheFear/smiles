import ply.lex as lex
import re

tokens = (
    'ATOM',
    'LPAREN',
    'RPAREN',
    'LBPAREN',
    'RBPAREN'
)

Valencia=dict([('C',4),('N',3),('O',2),('H',1),('Au' ,79),('Fe',2)])
t_LPAREN= r'\('
t_RPAREN = r'\)'
t_LBPAREN = r'\['
t_RBPAREN = r'\]'

def t_ATOM(t):
    r'[A-Z]|\[([A-Z][a-z]?)([A-Z])?(-*|\+*)?([1-9]?|[A-Z]+)?(-*|\+*)\]'  # A regex identifica um símbolo de elemento químico no formato [A] ou [Au] # 
    if '[' in t.value: 
       print("====>", t.value)
       mol=re.search('\[([A-Z][a-z]?)([A-Z])?(-*|\+*)?([1-9]|[A-Z]+)?(-*|\+*)\]', t.value)
       MolPrincipal=mol.group(1)
       MolSecun=mol.group(2)
       MolCarga=mol.group(3)
       MolRepetition=mol.group(4)
       MolCargaAlt=mol.group(5)
       print(MolPrincipal, "--", MolSecun, "--", MolCarga, "--", MolRepetition, "--", MolCargaAlt)  #mol.group(3), "=")
       erro=0
       if MolRepetition:
           if re.match(r"[0-9]+", MolRepetition):
               print("repeticao numero ", MolRepetition)
               reps=int(MolRepetition)
           elif re.match(r"[A-Z]+", MolRepetition):
               print("repeticao moleculas  ", MolRepetition)
               i=0
               while i <= len(MolRepetition)-1 and MolRepetition[0]==MolRepetition[i]:
                   i=i+1
               if i <= len(MolRepetition)-1:
                   print(" Erro de repetição de moléculas")
                   erro=1
               elif MolRepetition[0]==MolSecun:
                   reps = len(MolRepetition)+1
                   print(" Repetição de móleculas, número=", len(MolRepetition)+1)
               else:
                   print(" Repetição diferente de molécula a ser repetida")
                   erro=1
           else:
               print("Erro na repetição")
               erro=1
           if erro == 0 and Valencia[MolPrincipal] >= Valencia[MolSecun]*reps:
               t.value=Valencia[MolPrincipal] + Valencia[MolSecun]*reps
           else:
               print(" Valencia negativa")
       else:
           print(" Não tem repetição")
       t.value = t.value.strip('[]') # Remove os colchetes e devolve o valencia       
       print("t.value dentro dos []", t.value)       
    else:
       t.value = Valencia[t.value]
    return t

# Define uma regra para ignorar espaços em branco
t_ignore = ' \t'

# Define uma regra de nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Define uma regra de erro
def t_error(t):
    print(f"Caractere inesperado '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()    

# def t_ATOM(t):
#     r'[A-Z]LBPAREN[a-z]RBPAREN'
#     print("t.value", t.value)
# #    print(Valencia[t.value])
#     t.value=Valencia[t.value]
#     return t

# #t_ignore = ' \t'

# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)

# def t_error(t):
#     print("Caractere inválido: '%s'" % t.value[0])
#     t.lexer.skip(1)


