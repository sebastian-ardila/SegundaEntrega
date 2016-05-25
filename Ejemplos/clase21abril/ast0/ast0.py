
from astRec import *
tokens = (
    'ID','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ID    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
   ('left','PLUS','MINUS'),
  ('left','TIMES','DIVIDE'),
)

def p_ExpSuma(p):
    '''expression : expression PLUS expression'''
    p[0]=ExpSuma(p[1], p[3])

def p_ExpMult(p):
    '''expression : expression TIMES expression'''
    p[0]=ExpMult(p[1], p[3])

def p_expNumero(p):
    'expression : NUMBER'
    p[0] = ExpNumero(p[1])

def p_error(t):
    print("Error de sintaxis en: '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc('SLR')

raiz=yacc.parse('5+6*3+8')
print raiz

#print raiz.op1
#print raiz.op2

print 'recorrido preorden ...'

raiz.preorden()

#print raiz.calcular() #llama al p[0] del axioma

