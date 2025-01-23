
import ply.yacc as yacc
from Smileslex2 import tokens
from Smileslex2 import Valencia

def p_mol_smiles_seq(p):
     '''mol : ATOM
            | mol ATOM'''
     if (len(p) == 2):
        p[0] = { 'left': 0,  'right': 0 , 'atomo': p[1]}
        print(' mol : ATOM ',p[0])
     elif (len(p) == 3):
        print(' mol : mol ATOM  p[1]=', p[1], ' p[2]=', p[2])
        if (p[1]['atomo'] != 0):
             print(" Atomo ", p[1])
             if p[2]!=0:
                  if (p[1]['atomo']>= p[2]):
                       p[0]={'left': p[1]['atomo']-p[2], 'right': 0, 'atomo': 0}                
                  else:
                       print(" p[2]-p[1]['atomo'] ", p[2]-p[1]['atomo']) 
                       p[0]={'left': 0, 'right': p[2]- p[1]['atomo'], 'atomo': 0}                
             else:
                  print( " Atomo sem valencia ")
        else:
             print(" Molecula ", p[1])
             if p[2]!=0:
                  if (p[1]['right']>=p[2]):
                       p[0]={'left': p[1]['left'],'right': p[1]['right']-p[2], 'atomo': 0}
                  else:
                       p[0]={'left': p[1]['left'],'right': p[2]-p[1]['right'], 'atomo': 0}
             else:
                  print( " Atomo sem valencia ")
#                  p[0]={'left': p[1][
#          print( " Molecula ", )
#        # if (p[1]['right'] + p[1]['left']>= p[2]['left']+p[2]['right']):
        #    print(" entrou na comparacao ")
        #    p[0]['left'] = (p[1]['right']+p[1]['left'])-(p[2]['left']+p[2]['right'])
        #    p[0]['right'] = (p[2]['right']+p[2]['left'])-
#        else:
     else:
         print(" formacao gramatical errada ")

def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('Smiles Mol > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(" resultado = ", result)         


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

# data = """
# CCHO
# """
# lexer.input(data)
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print("Atomo e Valencia ", tok, Valencia[tok.value])

# result = parser.parse(data)
# print("Resultado da expressão:", result)
