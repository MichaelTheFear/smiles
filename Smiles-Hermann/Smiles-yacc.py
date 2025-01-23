
import ply.yacc as yacc
from Smileslex import tokens

def mol_smiles_seq(p):
    'mol : ATOM | mol ATOM'
    if (len(p) == 2):
         p[0].right = p[1].right
         p[0].left = p[1].left
    elif (len(p) == 3):
        if (p[1].right == p[2].left):
            p[0].left = p[1].left
            p[0].right = p[2].right
        else:
            print("erro de valencia em ", ATOM.value)
    else:
        print(" formacao errada ")


def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('Smiles Mol > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)


# def p_expression_plus(p):
#     'expression : expression PLUS expression'
#     p[0] = p[1] + p[3]

# def p_expression_minus(p):
#     'expression : expression MINUS expression'
#     p[0] = p[1] - p[3]

# def p_expression_number(p):
#     'expression : NUMBER'
#     p[0] = p[1]

# def p_error(p):
#     print("Erro de sintaxe!")

# parser = yacc.yacc()

data = """
CCHO
"""
# lexer.input(data)
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print("Atomo e Valencia ", tok, Valencia[tok.value])

# result = parser.parse(data)
# print("Resultado da expressão:", result)
