from sly import Lexer
import json
import re

tp = None # tabela periodica

with open("tabela_periodica.json") as tp_arquivo:
    tp = json.load(tp_arquivo)

def generate_regex_from_list(elem_list:list[str]) -> str:
    re_elem = []
    for elem in elem_list:
        re_elem.append(re.escape(elem))

    return '|'.join(re_elem)

organic_atoms = ["N","O","P","S","F","Cl","Br","I", "C"] # direto do artigo, tem mais?
inorganic_atoms = list(set(tp.keys()) - set(organic_atoms) - set("H"))
bonds = ["=", "#", "$", "/", "\\"]

class SmilerLex(Lexer):
    literals = {".","@","-","+",":","%","H",")","(","]","[", 'H'}

    semi_organic_symbols = rf'{generate_regex_from_list(organic_atoms)}'
    semi_symbol = rf'{generate_regex_from_list(inorganic_atoms)}'
    semi_bond = rf'{generate_regex_from_list(bonds)}'
    digit = r'\d'