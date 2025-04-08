
# este puno NO ES PARTE DEL TALLER mas sin embargo lo hicimos con pequeñas ayudas de youtube + ia
# para validar la gramatica libre mediante codigo

import sys
sys.dont_write_bytecode = True  # Evita que se cree la carpeta __pycache__

import os
import ply.lex as lex  # Analizador lexico
import ply.yacc as yacc  # Analizador sintactico
from graphviz import Digraph  # Para generar el arbol como imagen

# --- Definicion de tokens ---
tokens = (
    'ID', 'NUM',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS',
    'LPAREN', 'RPAREN'
)

# Expresiones regulares para los tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ID      = r'[a-zA-Z_]\w*'  # Identificadores
t_NUM     = r'\d+'  # Numeros enteros
t_ignore  = ' \t'  # Ignorar espacios y tabulaciones

# Contar saltos de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores lexicos
def t_error(t):
    t.lexer.skip(1)

# Crear el analizador lexico
lexer = lex.lex()

# --- Funcion para construir nodos del arbol ---
def node(name, children=None):
    return {"name": name, "children": children or []}

# --- Reglas gramaticales ---

# Produccion principal: asignacion
def p_S(p):
    'S : ID EQUALS E'
    p[0] = node("S", [
        node(f"id ({p[1]})"),
        node("="),
        p[3]
    ])

# Expresiones con suma o resta
def p_E_binop(p):
    '''E : E PLUS T
        | E MINUS T'''
    p[0] = node("E", [
        p[1],
        node(p[2]),
        p[3]
    ])

# Expresion simple (sin suma o resta)
def p_E_term(p):
    'E : T'
    p[0] = node("E", [p[1]])

# Terminos con multiplicacion o division
def p_T_binop(p):
    '''T : T TIMES F
        | T DIVIDE F'''
    p[0] = node("T", [
        p[1],
        node(p[2]),
        p[3]
    ])

# Termino simple (sin * o /)
def p_T_factor(p):
    'T : F'
    p[0] = node("T", [p[1]])

# Agrupacion con parentesis
def p_F_group(p):
    'F : LPAREN E RPAREN'
    p[0] = node("F → (E)", [p[2]])

# Factor que puede ser identificador o numero
def p_F_id_num(p):
    '''F : ID
        | NUM'''
    tipo = "id" if p.slice[1].type == "ID" else "num"
    p[0] = node(f"F → {tipo} ({p[1]})")

# Manejo de errores sintacticos
def p_error(p):
    print("Error de sintaxis")

# Crear el parser sin generar parsetab.py
parser = yacc.yacc(write_tables=False, debug=False)

# --- Funcion para generar el arbol en formato Graphviz ---
def render_tree(tree, dot=None, parent=None, node_id_gen=[0]):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='box')  # Estilo de los nodos

    node_id = str(node_id_gen[0])
    node_id_gen[0] += 1

    dot.node(node_id, tree["name"])

    if parent is not None:
        dot.edge(parent, node_id)

    for child in tree["children"]:
        render_tree(child, dot, node_id, node_id_gen)

    return dot

# --- Funcion principal ---
def main():
    # Solicitar entrada al usuario
    entrada = input("Escribe una expresion como 'z = a * (b + c) - d':\n> ")
    
    # Analizar la expresion
    resultado = parser.parse(entrada)

    # Si no hay errores, se genera el arbol
    if resultado:
        dot = render_tree(resultado)
        output_file = "arbol_GramaticaLibre"

        # Generar imagen PNG del arbol
        dot.render(output_file, format='png', cleanup=True)

        print(f"\nImagen generada: {output_file}.png")

        # Abrir la imagen automaticamente (solo en Windows)
        os.startfile(f"{output_file}.png")

# Ejecutar el programa
if __name__ == "__main__":
    main()