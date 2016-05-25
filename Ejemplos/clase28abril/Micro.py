# -*- coding: cp1252 -*-
#----------------------------------------------------------------------
# Micro AST
#----------------------------------------------------------------------
import lex as lex
import yacc as yacc
#Importa el archivo donde están las clases asociadas a los nodos del árbol
from MicroAst0 import *

#----------------------------------------------------------------------
# Analizador Lexicografico
#----------------------------------------------------------------------
#¿program --> classdecl *?

#program --> classdecl ListaDeclClase 
#ListaDeclClase --> classdecl ListaDeclclase
#ListaDeclClase -> epsilon

#[extends]
#extendsopr:extends | espsilon

#lista de elementos combinados que puede ser declaracion de cmapos o declaracion de metodos:
#(fieldDecl | methDecl)* 
#classDecl ::= class id [extends id] ‘{‘ (fieldDecl | methDecl)* ‘}’

#class Estudiante {
	#int edad;
	#int calcularNota(){}
	#int codigo;
	#int ejecutarcodigo(){}
#}
#----------------------------------------------------------------------
keywords = (
    'INTEGER','STRING','CLASS', 'RETURN',
    'PLUS','MINUS','TIMES','DIVIDE'
)   

tokens = keywords + (
    'NUMBER','ID'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'


# Tokens

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value.upper() in keywords:
        t.type = t.value.upper()
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Valor de entero muy grande", t.value
        t.value = 0
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lineno += t.value.count("\n")
    
def t_error(t):
    print "Caracter ilegal '%s'" % t.value[0]
    t.skip(1)

literals = ['(',')',';','{','}']
    
lex.lex()

#----------------------------------------------------------------------
# Analizador Sintatico
#----------------------------------------------------------------------


precedence = (
    ('left', 'PLUS','MINUS'),
    ('left', 'TIMES','DIVIDE')
)

def p_Program(p):
    'Program : DeclList'
    p[0] = Program(p[1])

def p_DeclList(p):
    'DeclList : ClassDecl DeclList'
    p[0] = DeclList(p[1], p[2])

def p_DeclList1(p):
    'DeclList : empty'
    p[0] = DeclListNull()
    
def p_ClassDecl(p):
    """ClassDecl : CLASS ID '{' FieldDecl MethDecl '}' """
    #nid =Id(p[2],p.lineno(1))
    #p[0]=classDecl(nId,p[4],p[5])
    p[0]=ClassDecl(Id(p[2],p.lineno(1)),p[4],p[5])

def p_FieldDecl(p):
    """FieldDecl : Type ID ';' """
    p[0]= FieldDecl(p[1], p[2])
    
def p_MethDecl(p):
    """MethDecl : Type ID '(' ')' '{' Body '}' """
    p[0]= MethDecl(p[1], p[2], p[6])

def p_Body(p):
    '''Body : FieldDecl Statement '''
    p[0]=Body(p[1], p[2])

def p_Statement(p): # En realidad instrucciones de muchas formas por ejemplo if_stmt
    """Statement : ID ';'"""
    p[0]=Statement(p[1])

def p_Type(p):
    '''Type : INTEGER
    | STRING
    | ID
    '''
    p[0] = Type(p[1])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print "Error de sintaxis ", p

yacc.yacc(method='SLR')

    
s = open("prueba.txt").read()
    
# Se construye el ast: raiz=p[0] de la primera regla
raiz = yacc.parse(s)
raiz.imprimir()




