from lark import Lark
from lark.tree import pydot__tree_to_png
import os
# Gramática 
grammar = r"""
    start: expr                -> start
    expr: expr "+" term        -> add
        | expr "-" term        -> sub
        | term
    term: term "*" factor      -> mul
        | term "/" factor      -> div
        | factor
    factor: "(" expr ")"       -> group
        | ID
        | NUMBER

    ID: /[a-zA-Z_][a-zA-Z_0-9]*/
    NUMBER: /\d+(\.\d+)?/

    %ignore " "
"""

# Crear el parser
parser = Lark(grammar, start='start', parser='lalr')

def main():
    # solicitar exprecion
    input_expr = input("Escribe una expresión aritmética: ")

    try:
        # Parsear la expresion
        tree = parser.parse(input_expr)

        # Mostrar arbol en consola
        print("\nÁrbol sintáctico:")
        print(tree.pretty())

        # Generar grafico
        output_file = "arbol_sintactico.png"
        pydot__tree_to_png(tree, output_file)
        print(f"\nImagen generada: {output_file}")

        # Abrir imagen automáticamente 
        os.startfile(output_file)

    except Exception as e:
        print("\nError al analizar la expresión:")
        print(e)

if __name__ == "__main__":
    main()
