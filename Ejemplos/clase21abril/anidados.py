# -*- coding: cp1252 -*-
# -----------------------------------------------------------------------------
#
# Analizador léxico de expresiones aritméticas 
# -----------------------------------------------------------------------------

# importa el primer módulo del ply
import ply.lex as lex
from sintactico_nodos import *
#from lexico import tokens

tokens = (
   'PARENIZQ','PARENDER', 'ID'
    )

# Tokens


t_PARENIZQ  = r'\('
t_PARENDER  = r'\)'
t_ID  = r'[a-z_][a-zA-Z0-9]*'

# Caracteres que se ignoran
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("No se reconoce el caracter '%s'" % t.value[0])
    t.lexer.skip(1)
    
# construye el analizador

analizador=lex.lex()

# Análisis sintáctico

def p_A(p):
    'A : ID'
    listA = []
    listA.add(p[1])
    p[0]=A(listA) #estamos instanciando un objeto de la clase A
    #p[0] = A1(p[1])

def p_AA(p):
    '''A : PARENIZQ A PARENDER'''
    listA = []
    listA.add(p[1])
    listA.add(p[2])
    listA.add(p[3])
    p[0] = A(listA)
    #p[0] = A(p[1],p[2],p[3])

def p_error(p):
    print("Error de sintaxis en '%s'" % p.value) 
    #print("Error de sintaxis en '%s'" % p)

import ply.yacc as yacc

yacc.yacc('SLR')
codigoFuente='((a))'
yacc.parse(codigoFuente)



