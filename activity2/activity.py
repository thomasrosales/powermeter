"""
1. Genere una lista con los valores no repetidos de la lista ‘repetidos’.
2. Genere una lista con los valores en común entre la lista ‘r’ y ‘repetidos’
3. Transforme ‘d_str’ en un diccionario.
"""

import json

repetidos = [1,2,3,"1","2","3",3,4,5]

r = [1, "5", 2, "3"]

d_str = '{"valor":125.3,"codigo":123}'


# Parte 1

unique_values = set(repetidos)
print(f"no repetidos: {unique_values}")

# Parte 2

common_values = [value for value in repetidos if value in r]
print(f"valores comunes: {common_values}")

# Parte 3

str_to_json = json.loads(d_str)
print("str to dict: ", str_to_json)
