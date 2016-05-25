# -*- coding: cp1252 -*-
# -*- coding: utf-8 -*- 

import ply.yacc as yacc
import os
import codecs
import re
from analizadorlexico import tokens
from sys import stdin
from ast import *

###############################################################################
#																			  
#							  Analizador Sintáctico							  
#																			
#
#									Hecho por:
#
#							Sebastian Ardila Agudelo.
#						   Alejandro Villegas Ocampo.
#
#
#					   Universidad Tecnológica de Pereira.
#									 2016.
#
#
###############################################################################


###############################################################################
#	
#	Tipo de variable = Tupla
#	Nombre de variable = precedence
#	Funcionamiento = 
#						* sirve para darle prioridad a los tokens que sea 
#						necesario
#
###############################################################################
precedence = (
			('left', 'UMINUS'),
			('right', 'IGUAL'),
			('left','OLOGICO'),
			('left', 'ILOGICO'),
			('left', 'IGUALIGUAL', 'DIFERENTE'),
			('left', 'MENORQUE', 'MENORIGUAL', 'MAYORQUE', 'MAYORIGUAL'),
			('left', 'SUM', 'MEN'),
			('left', 'MULT', 'DIV', 'MOD'),
			('right', 'NEGBOOL', 'NEW'),
			('left', 'LCOR', 'RCOR', 'LPAR', 'RPAR','DOT'),
			)

###############################################################################
#	
#	Nombre de funcion = program
#	Funcionamiento = 
#						* identifica una o varias declaraciones de clase
#
###############################################################################

def p_program(p):
	'''program : program classDecl \n'''
	sons=[p[1],p[2]]
	p[0] = Node(sons, "program")

	#print "program"

###############################################################################
#	
#	Nombre de funcion = programNull
#	Funcionamiento = 
#						* reduce en program
#
###############################################################################

def p_programNull(p):
	'''program : empty'''
	p[0] = Null()

	#print "program null"

###############################################################################
#	
#	Nombre de funcion = classDecl
#	Funcionamiento = 
#						* identifica los componentes de una declaracion de 
#						clase
#
###############################################################################

def p_classDecl(p):
	'''classDecl : CLASS ID extendsIdOp LKEY listFieldOrMethDecl RKEY'''
	sons = [ID(p[2],p.lineno(1)), p[3],p[5]]
	p[0] = Node(sons, "classDecl")
	
	#print "Declaracion de Clase"

###############################################################################
#	
#	Nombre de funcion = extendsIdOp
#	Funcionamiento = 
#						* identifica dos tokens en la declaracion de clase
#
###############################################################################

def p_extendsIdOp(p):
	'''extendsIdOp : EXTENDS ID'''
	p[0] = Node(ID(p[2],p.lineno(1)), "extendsIdOp")

	#print "Extends ID en Declaracion de Clase"

###############################################################################
#	
#	Nombre de funcion = extendsIdOpNull
#	Funcionamiento = 
#						* produccion que genera vacio
#
###############################################################################

def p_extendsIdOpNull(p):
	'''extendsIdOp : empty'''
	p[0] = Null()

	#print 'extendsIdOpNull'

###############################################################################
#	
#	Nombre de funcion = listFieldOrMethDecl
#	Funcionamiento = 
#						* identifica una o varias declaraciones de metodo o 
#						campo
#
###############################################################################

def p_listFieldOrMethDecl(p):
	'''listFieldOrMethDecl : listFieldOrMethDecl fieldOrMethDecl'''
	sons = [p[1],p[2]]
	p[0] = Node(sons, "listFieldOrMethDecl")

	#print 'lista de declaraciones de Campo o Metodo'

###############################################################################
#	
#	Nombre de funcion = listFieldOrMethDeclNull
#	Funcionamiento = 
#						* produccion que genera vacio
#
###############################################################################

def p_listFieldOrMethDeclNull(p):
	'''listFieldOrMethDecl : empty'''
	p[0] = Null()

	#print 'listFieldOrMethDeclNull'

###############################################################################
#	
#	Nombre de funcion = fieldOrMethDecl_field
#	Funcionamiento = 
#						* identifica una declaracion de campo
#
###############################################################################

def p_fieldOrMethDecl_field(p):
	'''fieldOrMethDecl : fieldDecl'''
	p[0] = Node(p[1], "fieldOrMethDecl_field")

	#print 'Declaracion de campo'

###############################################################################
#	
#	Nombre de funcion = listFieldOrMethDecl_meth
#	Funcionamiento = 
#						* identifica una declaracion de metodo
#
###############################################################################

def p_listFieldOrMethDecl_meth(p):
	'''fieldOrMethDecl : methDecl'''
	p[0] = Node(p[1], "listFieldOrMethDecl_meth")

	#print 'Declaracion de metodo'

###############################################################################
#	
#	Nombre de funcion = fieldDecl
#	Funcionamiento = 
#						* identifica una o varias declaraciones de campo con sus 
#						respectivos componentes.
#
###############################################################################

def p_fieldDecl(p):
	'''fieldDecl : type ID COMMA ID listId DOTCOMMA'''
	sons = [p[1],ID(p[2],p.lineno(1)),ID(p[4],p.lineno(1)),p[5]]
	p[0] = Node(sons, "fieldDecl"+p[2])

	#print 'componentes de declaracion de campo'

###############################################################################
#	
#	Nombre de funcion = listId
#	Funcionamiento = 
#						* identifica uno o varios identificadores separados 
#						por comas
#
###############################################################################

def p_listId(p):
	'''listId : COMMA ID listId'''
	sons = [ID(p[2],p.lineno(1)),p[3]]
	p[0] = Node(sons, "List ID"+p[2])

	#print 'lista de identificadores'

###############################################################################
#	
#	Nombre de funcion = listIdNull
#	Funcionamiento = 
#						* produccion que genera vacio
#
###############################################################################

def p_listIdNull(p):
	'''listId : empty'''
	p[0] = Null()

	#print "listIdNull"

###############################################################################
#	
#	Nombre de funcion = methDecl
#	Funcionamiento = 
#						* identifica una declaracion de metodo con sus 
#						respectivos componentes
#
###############################################################################

def p_methDecl(p):
	'''methDecl : type ID LPAR formals RPAR block'''
	sons = [p[1],ID(p[2],p.lineno(1)),p[4],p[6]]
	p[0] = Node(sons, "Meth Decl"+p[2])

	#print 'componentes de declaracion de metodo'

###############################################################################
#	
#	Nombre de funcion = formals
#	Funcionamiento = 
#						* identifica un tipo de dato seguido del dato o
#						identificador, seguido o no de una lista con los 
#						mismos elementos. 
#
###############################################################################

def  p_formals(p):
	'''formals : type ID COMMA type ID listTypeId'''
	sons = [p[1],ID(p[2],p.lineno(1)),p[4],ID(p[5],p.lineno(1)),p[6]]
	p[0] = Node(sons, "formals"+p[2])

	#print 'formals'

	## if (len(p) == 7):
	## 	nId = Id(p[2],p.lineno(1))
	## 	p[0] = formals(p[1], nId, p[4], nId, p[6])

	## elif (len(p) = 2):
	## 	p[0] = formalsNull()

###############################################################################
#	
#	Nombre de funcion = formalsNull
#	Funcionamiento = 
#						* produccion que genera vacio
#
###############################################################################

def p_formalsNull(p):
	'''formals : empty'''
	p[0] = Null()

	#print "formalsNull"

###############################################################################
#	
#	Nombre de funcion = listTypeId
#	Funcionamiento = 
#						* identifica una produccion que genera un tipo y un ID
#						seguido o no por una lista con los mismos elementos
#
###############################################################################

def p_listTypeId(p):
	'''listTypeId : COMMA type ID listTypeId'''
	sons = [p[2],ID(p[3],p.lineno(1)),p[4]]
	p[0] = Node(sons, "List Type ID "+p[3])

	#print 'lista de tipos'

	## if (len(p) == 5):
	## 	nId = Id(p[3],p.lineno(1))
	## 	p[0] = listTypeId(p[2], nId, p[4])

	## elif (len(p) = 2):
	## 	p[0] = listTypeIdNull()

###############################################################################
#	
#	Nombre de funcion = listTypeIdNull
#	Funcionamiento = 
#						* produccion que genera vacio
#
###############################################################################

def p_listTypeIdNull(p):
	'''listTypeId : empty'''
	p[0] = Null()

	#print "listTypeIdNull"

###############################################################################
#	
#	Nombre de funcion = type_INT
#	Funcionamiento = 
#						* identifica una produccion que genera un entero
#
###############################################################################
def p_type_INT(p):
	'''type : INT'''
	p[0] = Node(p[1], "type INT")

	#print 'tipo entero'

###############################################################################
#	
#	Nombre de funcion = type_BOOLEAN
#	Funcionamiento = 
#						* identifica una produccion que genera un booleano
#
###############################################################################

def p_type_BOOLEAN(p):
	'''type : BOOLEAN'''
	p[0] = Node(p[1], "type BOOLEAN")

	#print 'tipo booleano'

###############################################################################
#	
#	Nombre de funcion = type_STRING
#	Funcionamiento = 
#						* identifica una produccion que genera un STRING
#
###############################################################################

def p_type_STRING(p):
	'''type : STRING'''
	p[0] = Node(p[1], "type STRING")

	#print 'tipo string'

###############################################################################
#	
#	Nombre de funcion = type_ID
#	Funcionamiento = 
#						* identifica una produccion que genera un ID
#
###############################################################################

def p_type_type_ID(p):
	'''type : type ID'''
	sons = [p[1],ID(p[2],p.lineno(1))]
	p[0] = Node(sons, "type ID")

	#print 'tipo ID'

###############################################################################
#	
#	Nombre de funcion = type_type_LCOR_RCOR
#	Funcionamiento = 
#						* identifica una produccion que genera un par de
#						corchetes
#
###############################################################################

def p_type_type_LCOR_RCOR(p):
	'''type : type LCOR RCOR'''
	p[0] = Node(p[1], "type []")

	#print 'tipo []'

###############################################################################
#	
#	Nombre de funcion = block
#	Funcionamiento = 
#						* identifica una produccion que genera un bloque de
#						elementos con sus respectivos componentes
#
###############################################################################

def p_block(p):
	'''block : LKEY varDecl listVarDecl stmt listStmt RKEY'''
	sons = [p[2],p[3],p[4],p[5]]
	p[0] = Node(sons, "block")

	#print 'block'

###############################################################################
#	
#	Nombre de funcion = listVarDecl
#	Funcionamiento = 
#						* identifica una produccion que genera una declaracion
#						de variable o una posible lista de declaraciones de 
#						variables
#
###############################################################################

def p_listVarDecl(p):
	'''listVarDecl : listVarDecl varDecl \n'''
	sons = [p[1],p[2]]
	p[0] = Node(sons, "list Var Decl")

	#print 'lista de declaraciones de variable'

	## if (len(p) == 3):
	## 	p[0] = listVarDecl(p[1], p[2])

	## elif (len(p) = 2):
	## 	p[0] = listVarDeclNull()

###############################################################################
#	
#	Nombre de funcion = listVarDeclNull
#	Funcionamiento = 
#						* identifica una produccion que genera vacio
#
###############################################################################

def p_listVarDeclNull(p):
	'''listVarDecl : empty'''
	p[0] = Null()

	#print "listVarDeclNull"

###############################################################################
#	
#	Nombre de funcion = listStmt
#	Funcionamiento = 
#						* identifica una produccion que genera un statement
#						o una lista de statement
#
###############################################################################

def p_listStmt(p):
	'''listStmt : listStmt stmt'''
	sons = [p[1],p[2]]
	p[0] = Node(sons, "List Stmt")

	#print 'lista de statement'

	## if (len(p) == 3):
	## 	p[0] = listStmt(p[1], p[2])

	## elif (len(p) = 2):
	## 	p[0] = listStmtNull()

###############################################################################
#	
#	Nombre de funcion = listStmtNull
#	Funcionamiento = 
#						* identifica una produccion que genera vacio
#
###############################################################################	

def p_listStmtNull(p):
	'''listStmt : empty'''
	p[0] = Null()
	
	#print "listStmtNull"

###############################################################################
#	
#	Nombre de funcion = varDecl
#	Funcionamiento = 
#						* identifica una produccion que genera una declaracion
#						de variable con sus respectivos componentes
#
###############################################################################	

def p_varDecl(p):
	'''varDecl : type ID equalExprOp COMMA ID equalExprOp listIdEqExprOp DOTCOMMA'''
	sons = [p[1],ID(p[2],p.lineno(1)),p[3],ID(p[5],p.lineno(1)),p[6],p[7]]
	p[0] = Node(sons, "Var Decl "+p[2])

	#print 'declaracion de variable'

	## nId = Id(p[2],p.lineno(1))
	## p[0] = varDecl(p[1], nId, p[3], nId, p[6], p[7])

###############################################################################
#	
#	Nombre de funcion = equalExprOp
#	Funcionamiento = 
#						* identifica una produccion que genera una asignacion
#						de una expresion
#
###############################################################################	

def p_equalExprOp(p):
	'''equalExprOp : IGUAL expr'''
	p[0] = Node(p[2], "Equal Expr OP")

	#print 'asignacion de una expresion'

	## if (len(p) == 3):
	## 	p[0] = equalExprOp(p[1], p[2])

	## elif (len(p) = 2):
	## 	p[0] = equalExprOpNull()

###############################################################################
#	
#	Nombre de funcion = equalExprOpNull
#	Funcionamiento = 
#						* identifica una produccion que genera vacio
#
###############################################################################	

def p_equalExprOpNull(p):
	'''equalExprOp : empty'''
	p[0] = Null()

	#print "equalExprOpNull"

###############################################################################
#	
#	Nombre de funcion = listIdEqExprOp
#	Funcionamiento = 
#						* identifica una produccion que genera una asignacion
#						de una expresion a uno o varios id 
#
###############################################################################	

def p_listIdEqExprOp(p):
	'''listIdEqExprOp : listIdEqExprOp COMMA ID equalExprOp '''
	sons = [p[1],ID(p[3],p.lineno(1)),p[4]]
	p[0] = Node(sons, "List ID Equal Expr OP")

	#print 'lista asignacion de una o mas expresiones'

	## if (len(p) == 5):
	## 	nId = Id(p[2],p.lineno(1))
	## 	p[0] = listIdEqExprOp(nId, p[3], p[4])

	## elif (len(p) = 2):
	## 	p[0] = listIdEqExprOpNull()

###############################################################################
#	
#	Nombre de funcion = listIdEqExprOpNull
#	Funcionamiento = 
#						* identifica una produccion que genera vacio
#
###############################################################################	

def p_listIdEqExprOpNull(p):
	'''listIdEqExprOp : empty'''
	p[0] = Null()

	#print "listIdEqExprOpNull"

###############################################################################
#	
#	Nombre de funcion = stmt_assign
#	Funcionamiento = 
#						* identifica una produccion que genera una asignacion
#						seguido de un punto y coma
#
###############################################################################	

def p_stmt_assign(p):
	'''stmt : assign DOTCOMMA'''
	p[0] = Node(p[1], "Stmt Assign")

	#print "asignacion stmt"

	## if (len(p) == 3):

	## 	#stmt : assign ';'
	## 	if (len(p[1]) == 4):
	## 		p[0] = stmt_assign(p[1])

	## 	#stmt : call ';'
	## 	if (len(p[1]) == 5):
	## 		p[0] = stmt_call(p[1])

	## 	#stmt : breakOrContinue ';'
	## 	if (len(p[1]) == 2):
	## 		p[0] = stmt_breakOrContinue(p[1])

	## #stmt : RETURN exprOp ';'
	## elif (len(p) = 4):
	## 	p[0] = stmt_return(p[2])

	## # stmt : IF LPAR expr RPAR stmt elseStmtOp
	## elif (len(p) == 7):
	## 	p[0] = stmt_ifElse(p[3], p[5], p[6])

	## #stmt : WHILE LPAR expr RPAR stmt
	## elif (len(p) == 6):
	## 	p[0] = stmt_while(p[3], p[5])

	## #stmt : block
	## elif (len(p) == 2):
	## 	p[0] = stmt_block(p[1])

###############################################################################
#	
#	Nombre de funcion = stmt_call
#	Funcionamiento = 
#						* identifica una produccion que genera un llamado
#						seguido de un punto y coma
#
###############################################################################	

def p_stmt_call(p):
	'''stmt : call DOTCOMMA'''
	p[0] = Node(p[1], "Stmt Call")

	#print "call stmt"

###############################################################################
#	
#	Nombre de funcion = stmt_RETURN
#	Funcionamiento = 
#						* identifica una produccion que genera un retorno 
#						que puede o no contener lo que retorna
#
###############################################################################	

def p_stmt_RETURN(p):
	'''stmt : RETURN exprOp DOTCOMMA'''
	p[0] = Node(p[2], "Stmt Return")

	#print "return stmt"

###############################################################################
#	
#	Nombre de funcion = stmt_IF
#	Funcionamiento = 
#						* identifica una produccion que genera condicional
#						if y sus respectivos componentes
#
###############################################################################	

def p_stmt_IF(p):
	'''stmt : IF LPAR expr RPAR stmt elseStmtOp'''
	sons = [p[3],p[5],p[6]]
	p[0] = Node(sons, "Stmt if")

	#print "if stmt"

###############################################################################
#	
#	Nombre de funcion = stmt_WHILE
#	Funcionamiento = 
#						* identifica una produccion que genera un while y sus
#						respectivos componentes
#
###############################################################################	

def p_stmt_WHILE(p):
	'''stmt : WHILE LPAR expr RPAR stmt'''
	sons = [p[3],p[5]]
	p[0] = Node(sons, "Stmt while")

	#print "while stmt"

###############################################################################
#	
#	Nombre de funcion = stmt_breakOrContinue
#	Funcionamiento = 
#						* identifica una produccion que genera o un break
#						o un continue, pero seguido de un punto y coma.
#
###############################################################################	

def p_stmt_breakOrContinue(p):
	'''stmt : breakOrContinue DOTCOMMA'''
	p[0] = Node(p[1], "Stmt [Break|Continue]")

	#print "break|continue"

###############################################################################
#	
#	Nombre de funcion = stmt_block
#	Funcionamiento = 
#						* identifica una produccion que genera un bloque de
#						codigo
#
###############################################################################	

def p_stmt_block(p):
	'''stmt : block'''
	p[0] = Node(p[1], "Stmt Block")

	#print "block stmt"

###############################################################################
#	
#	Nombre de funcion = exprOp
#	Funcionamiento = 
#						* identifica una produccion que genera una expresion
#
###############################################################################	

def p_exprOp(p):
	'''exprOp : expr'''
	p[0] = Node(p[1], "Expr OP")

	#print 'expresion'

	## if (len(p[1]) == 2):
	## 	#p[0] = exprOp(p[1])

	## elif (len(p[1]) < 2):
	## 	#p[0] = exprOpNull()

###############################################################################
#	
#	Nombre de funcion = exprOpNull
#	Funcionamiento = 
#						* identifica una produccion que genera una vacio
#
###############################################################################	


def p_exprOpNull(p):
	'''exprOp : empty'''
	p[0] = Null()

	#print "exprOpNull"

###############################################################################
#	
#	Nombre de funcion = elseStmtOpElse
#	Funcionamiento = 
#						* identifica una produccion que genera un else
#
###############################################################################	

def p_elseStmtOpElse(p):
	'''elseStmtOp : ELSE'''
	p[0] = Node(p[1], "Else Stmt OP ELSE")

	#print 'else'

	## if (len(p) == 3):
	## 	#p[0] = elseStmtOp(p[2])

	## elif (len(p) == 2):
	## 	#p[0] = exprOpNull()

###############################################################################
#	
#	Nombre de funcion = elseStmtOpStmt
#						* identifica una produccion que genera un stmt
#
###############################################################################		

def p_elseStmtOpStmt(p):
	'''elseStmtOp : stmt'''
	p[0] = Node(p[1], "Else Stmt OP Stmt")

	#print "stmt"

###############################################################################
#	
#	Nombre de funcion = breakOrContinue_Break
#	Funcionamiento = 
#						* identifica una produccion que genera un break
#
###############################################################################	

def p_breakOrContinue_Break(p):
	'''breakOrContinue : BREAK'''
	p[0] = Node(p[1], " [BREAK|CONTINUE] -> BREAK")

	#print 'break'

###############################################################################
#	
#	Nombre de funcion = breakOrContinue_Continue
#	Funcionamiento = 
#						* identifica una produccion que genera un continue
#
###############################################################################	

def p_breakOrContinue_Continue(p):
	'''breakOrContinue : CONTINUE'''
	p[0] = Node(p[1], " [BREAK|CONTINUE] -> CONTINUE")

	#print 'continue'

###############################################################################
#	
#	Nombre de funcion = assign
#	Funcionamiento = 
#						* identifica una produccion que genera una asignacion
#						de una expresion a un tipo de location
#
###############################################################################	

def p_assign(p):
	'''assign : location IGUAL expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "assign")

	#print 'asignacion de una expresion a un location'

###############################################################################
#	
#	Nombre de funcion = location_ID
#	Funcionamiento = 
#						* identifica una produccion que genera un identificador
#
###############################################################################

def p_location_ID(p):
	'''location : ID'''
	p[0] = Node(ID(p[1],p.lineno(1)), "Location ID")

	#print "location id"

###############################################################################
#	
#	Nombre de funcion = location_expr_DOT_ID
#	Funcionamiento = 
#						* identifica una produccion que genera un llamado
#						al identificador de una expresion
#
###############################################################################

def p_location_expr_DOT_ID(p):
	'''location : expr DOT ID'''
	sons = [p[1],ID(p[3],p.lineno(1))]
	p[0] = Node(sons, "Location expr.ID")

	#print "location expr.id"

###############################################################################
#	
#	Nombre de funcion = location_expr_LCOR_RCOR
#	Funcionamiento = 
#						* identifica una produccion que genera un llamado
#						al indice de una expresion
#
###############################################################################

def p_location_expr_LCOR_RCOR(p):
	'''location : expr LCOR expr RCOR'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "location expr [expr]")

	#print "location expr [expr]"

###############################################################################
#	
#	Nombre de funcion = call
#	Funcionamiento = 
#						* identifica una produccion que genera un metodo que
#						se le envian parametros
#
###############################################################################

def p_call(p):

	'''call : method LPAR actuals RPAR'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "call")

	#print 'call'

###############################################################################
#	
#	Nombre de funcion = method_ID
#	Funcionamiento = 
#						* identifica una produccion que genera un identificador
#
###############################################################################

def p_method_ID(p):
	'''method : ID'''
	p[0] = Node(ID(p[1],p.lineno(1)), "method ID")

	#print 'method ID'

###############################################################################
#	
#	Nombre de funcion = method_expr_DOT_ID
#	Funcionamiento = 
#						* identifica una produccion que genera un llamado
#						al identificador de una expresion
#
###############################################################################

def p_method_expr_DOT_ID(p):
	'''method : expr DOT ID'''
	sons = [p[1],ID(p[3],p.lineno(1))]
	p[0] = Node(sons, "method expr.ID")

	#print 'method expr.ID'

###############################################################################
#	
#	Nombre de funcion = actuals
#	Funcionamiento = 
#						* identifica una produccion que genera una o varias
#						expresiones separadas por comas
#
###############################################################################

def p_actuals(p):
	'''actuals : expr COMMA expr listExpr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "actuals")

	## if (len(p) == 5):
	## 	p[0] = actuals(p[1], p[3], p[4])

	## elif (len(p) == 2):
	## 	p[0] = actualsNull()

	#print 'actuals'

###############################################################################
#	
#	Nombre de funcion = actualsNull
#	Funcionamiento = 
#						* identifica una produccion que genera vacio
#
###############################################################################

def p_actualsNull(p):
	'''actuals : empty'''
	p[0] = Null()
	#print "actualsNull"

###############################################################################
#	
#	Nombre de funcion = listExpr
#	Funcionamiento = 
#						* identifica una produccion que genera una lista de
#						expresiones separadas por coma
#
###############################################################################

def p_listExpr(p):
	'''listExpr : COMMA expr listExpr'''
	sons = [p[2],p[3]]
	p[0] = Node(sons, "List Expr")

	## if (len(p) == 4):
	## 	p[0] = listExpr(p[2], p[3])

	## elif (len(p) == 2):
	## 	p[0] = listExprNull()

	#print 'lista de expresiones'

###############################################################################
#	
#	Nombre de funcion = listExprNull
#	Funcionamiento = 
#						* identifica una produccion que genera vacio
#
###############################################################################

def p_listExprNull(p):
	'''listExpr : empty'''
	p[0] = Null

	#print "listExprNull"

###############################################################################
#	
#	Nombre de funcion = expr
#	Funcionamiento = 
#						* identifica una produccion que genera un location
#
###############################################################################

def p_expr(p):
	'''expr : location'''
	p[0] = Node(p[1], "expr location")
	#print "expr LOCATION"

## def p_expr_binary(p):

## 	'''expr : expr binary expr'''
## 	#'''expr : binary expr'''
## 	#p[0] = expr_binary(p[1], p[2], p[3])
## 	#print "expr BINARY"

###############################################################################
#	
#	Nombre de funcion = expr_binary_SUM
#	Funcionamiento = 
#						* identifica una produccion que genera un suma de 
#						expresiones
#
###############################################################################

def p_expr_binary_SUM(p):
	'''expr : expr SUM expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr sum expr")

	#print "expr + expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_MEN
#	Funcionamiento = 
#						* identifica una produccion que genera una resta de 
#						expresiones
#
###############################################################################

def p_expr_binary_MEN(p):
	'''expr : expr MEN expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr men expr")

	#print "expr - expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_MULT
#	Funcionamiento = 
#						* identifica una produccion que genera una 
#						multiplicacion de expresiones
#
###############################################################################

def p_expr_binary_MULT(p):
	'''expr : expr MULT expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr mult expr")

	#print "expr * expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_DIV
#	Funcionamiento = 
#						* identifica una produccion que genera una division
#						de expresiones
#
###############################################################################

def p_expr_binary_DIV(p):
	'''expr : expr DIV expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr div expr")

	#print "expr / expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_MOD
#	Funcionamiento = 
#						* identifica una produccion que genera un modulo
#						entre expresiones
#
###############################################################################

def p_expr_binary_MOD(p):
	'''expr : expr MOD expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr mod expr")

	#print "expr %  expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_ILOGICO
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						and entre expresiones
#
###############################################################################

def p_expr_binary_ILOGICO(p):
	'''expr : expr ILOGICO expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr and expr")

	#print "expr && expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_OLOGICO
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						or entre expresiones
#
###############################################################################

def p_expr_binary_OLOGICO(p):
	'''expr : expr OLOGICO expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr or expr")

	#print "expr || expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_MENORQUE
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						menor que entre expresiones
#
###############################################################################

def p_expr_binary_MENORQUE(p):
	'''expr : expr MENORQUE expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr < expr")

	#print "expr < expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_MENORIGUAL
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						menor igual entre expresiones
#
###############################################################################

def p_expr_binary_MENORIGUAL(p):
	'''expr : expr MENORIGUAL expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr <= expr")

	#print "expr <= expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_MAYORQUE
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						mayor que entre expresiones
#
###############################################################################

def p_expr_binary_MAYORQUE(p):
	'''expr : expr MAYORQUE expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr > expr")

	#print "expr > expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_MAYORIGUAL
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						mayor o igual entre expresiones
#
###############################################################################

def p_expr_binary_MAYORIGUAL(p):
	'''expr : expr MAYORIGUAL expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr >= expr")

	#print "expr >= expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_IGUALIGUAL
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						igual igual entre expresiones
#
###############################################################################

def p_expr_binary_IGUALIGUAL(p):
	'''expr : expr IGUALIGUAL expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "expr == expr")

	#print "expr == expr"

###############################################################################
#	
#	Nombre de funcion = expr_binary_DIFERENTE
#	Funcionamiento = 
#						* identifica una produccion que genera una condicion
#						de diferente entre expresiones
#
###############################################################################

def p_expr_binary_DIFERENTE(p):
	'''expr : expr DIFERENTE expr'''
	sons = [p[1],p[3]]
	p[0] = Node(sons, "exr != expr")

	#print "expr != expr"

###############################################################################
#	
#	Nombre de funcion = expr_call
#	Funcionamiento = 
#						* identifica una produccion que genera un call
#
###############################################################################

def p_expr_call(p):
	'''expr : call'''
	p[0] = Node(p[1], "expr call")

	#print "expr call"

###############################################################################
#	
#	Nombre de funcion = expr_this
#	Funcionamiento = 
#						* identifica una produccion que genera un this
#
###############################################################################

def p_expr_this(p):
	'''expr : THIS'''
	p[0] = Node(p[1], "expr this")

	#print "expr this"

###############################################################################
#	
#	Nombre de funcion = expr_new_id
#	Funcionamiento = 
#						* identifica una produccion que genera un nuevo
#						identificador 
#
###############################################################################

def p_expr_new_id(p):
	'''expr : NEW ID LPAR RPAR'''
	p[0] = Node(ID(p[2],p.lineno(1)), " expr new ID ()")

	#print "expr new ID"

###############################################################################
#	
#	Nombre de funcion = expr_new_type
#	Funcionamiento = 
#						* identifica una produccion que genera un nuevo tipo
#
###############################################################################

def p_expr_new_type(p):
	'''expr : NEW type LCOR expr RCOR'''
	sons = [p[2],p[4]]
	p[0] = Node(sons)

	#print "expr new type"

###############################################################################
#	
#	Nombre de funcion = expr_DOT_LENGTH
#	Funcionamiento = 
#						* identifica una produccion que genera la longitud
#						de una expresion
#
###############################################################################

def p_expr_DOT_LENGTH(p):
	'''expr : expr DOT LENGTH'''
	p[0] = Node(p[1], "expr.length")

	#print "expr.length"

###############################################################################
#	
#	Nombre de funcion = expr_uminus
#	Funcionamiento = 
#						* identifica una produccion que genera cambio de signo
#						en una expresion
#
###############################################################################

def p_expr_uminus(p):
	'''expr : UMINUS expr'''
	p[0] = Node(p[2], "minus expr")

	#print "- expr"

###############################################################################
#	
#	Nombre de funcion = expr_negbool
#	Funcionamiento = 
#						* identifica una produccion que genera la negacion
#						de una expresion
#
###############################################################################

def p_expr_negbool(p):
	'''expr : NEGBOOL expr'''
	p[0] = Node(p[2], "negbool expr")

	#print "! expr"

###############################################################################
#	
#	Nombre de funcion = expr_literal
#	Funcionamiento = 
#						* identifica una produccion que genera un literal
#
###############################################################################

def p_expr_literal(p):
	'''expr : literal'''
	p[0] = Node(p[1], "expr literal")

	#print "expr literal"

###############################################################################
#	
#	Nombre de funcion = expr_expr
#	Funcionamiento = 
#						* identifica una produccion que genera una expresion
#						entre parentesis
#
###############################################################################

def p_expr_expr(p):
	'''expr : LPAR expr RPAR'''
	p[0] = Node(p[2], "(expr)")

	#print "expr (expr)"

#16
# def p_binary(p):

# 	'''binary : SUM
# 				| MEN
# 				| MULT
# 				| DIV
# 				| MOD
# 				| ILOGICO
# 				| OLOGICO
# 				| MENORQUE
# 				| MENORIGUAL
# 				| MAYORQUE
# 				| MAYORIGUAL
# 				| IGUALIGUAL
# 				| DIFERENTE
# 	'''
## 	#p[0] = binary(p[1])

# 	print 'binary'

#17
# def p_unary(p):

# 	'''unary : UMINUS
# 				| NEGBOOL
# 	'''
## 	#p[0] = unary(p[1])

# 	print 'unary'

###############################################################################
#	
#	Nombre de funcion = literal
#	Funcionamiento = 
#						* identifica una produccion que genera su 
#						correspondiente literal
#
###############################################################################

def p_literal(p): 

	'''literal : NUMERO
				| CAD
				| TRUE
				| FALSE
				| NULL
	'''
	
	p[0] = Node(p[1], "literal")

	#print "literal"

###############################################################################
#	
#	Nombre de funcion = empty
#	Funcionamiento = 
#						* identifica una produccion que genera vacio
#
###############################################################################

def p_empty(p):
	'''empty :'''
	#p[0] = empty()
	pass

def p_error(p):

	print "Error de sintaxis ", p
	print "Error en la linea "+str(p.lineno)
	# print "Error: "
	# while True:
	# 	tok = parser.token()
	# 	if not tok : break

###############################################################################
#	
#	Nombre de funcion = buscarFicheros
#	Funcionamiento = 
#						* funcion que lista las pruebas y las muestra en 
#						pantalla para elegir entre una de ellas y analizarla
#
###############################################################################

def buscarFicheros():
	ficheros = []
	numArchivo = ''
	respuesta = False
	cont = 1

	for base, dirs, files in os.walk('/home/villegas/Documentos/Compiladores-Glindres/MJ/Segunda Entrega/Analizador Sintactico/test/'):
		ficheros.append(files)
	
	for file in files:
		print str(cont)+". "+file
		cont = cont+1

	while respuesta == False:
		numArchivo = raw_input('\nNumero del Test: ')
		for file in files:
			if file == files[int(numArchivo)-1]:
				respuesta = True
				break

	print "Has escogido \"%s\" \n" %files[int(numArchivo)-1]

	return files[int(numArchivo)-1]
		
#CREAR SINTACTICO---------------------------------


print "\nBienvenido al Analizador Sintáctico."
print "Por favor, elige la prueba"
print "Presiona Ctrl+z para salir\n"


directorio = "/home/villegas/Documentos/Compiladores-Glindres/MJ/Segunda Entrega/Analizador Sintactico/test/"
archivo = buscarFicheros()
test = directorio+archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
#cadena = str(cadena)
fp.close()

yacc.yacc()

raiz = yacc.parse(cadena, debug=1)
raiz.imprimirPostOrden(" ")
#raiz.imprimirPostOrden()

#CONSTRUIR EL ANALIZADOR PARSER---------------
#parser = yacc.yacc()

#result = parser.parse(stdin.read(),lexer=le)
#IMPRIME EL PARSER----------------------------
#print(result)