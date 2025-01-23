from rdkit.Chem import GetPeriodicTable

def simbolos_tabela_periodica() -> list[str]:
    tabela_periodica = GetPeriodicTable()
    simbolos = {}
    n_tabela_periodica = 118 # numero de elementos da tabela periodica
    for i in range(1, n_tabela_periodica+1):
        simbolo = tabela_periodica.GetElementSymbol(i)
        simbolos[simbolo] = {
            'valencia': list(tabela_periodica.GetValenceList(i)),
            'numero_atomico': i
        }
    
    return simbolos


import json
with open('tabela_periodica.json','w') as arquivo_json:
    print()
    json.dump(simbolos_tabela_periodica(),arquivo_json)
    