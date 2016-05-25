# -*- coding: cp1252 -*-
#Ver 6.10 AST Construction del manual de referencia

class Node: 
    pass

class NullNode(Node):
    "Representa un nodo nulo, despues de una produccion vacia"
    def __init__(self):
        self.type = 'void'
    
    def imprimir(self):
        print 'null node'

class Id(Node):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno
    def imprimir(self):
        print 'id'

class Binop(Node):
    """Operaciones binarias por ejemplo: + - * ,  = += -= """
    # Lista de operadores de asignacion.
    #ASSIGN_OPS = ['=', '+=', '-=']

    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def imprimir(self):
        print 'Nodo Operador con dos operandos'
        self.left.imprimir()
        self.right.imprimir()

class Program(Node):
    """Programa contiene una lista de declaraciones,
    cambiar para disminuir la profundidad del arbol"""
    def __init__(self, declList):
        self.declList = declList
        self.name="Program"
    
    def imprimir(self):
        print 'axioma Programa'
        self.declList.imprimir()
    
    
class Statement(Node):
    """Nodo que representa un solo tipo de statement """
    def __init__(self, expr):
        self.expr = expr
        self.name="Statement"
    def imprimir(self):
        print 'Statement: ' + self.expr

class NodeList(Node):
    """Lista de nodos. Se puede usar para las diferentes listas como DeclList, ParamList, MethList etc.
    Esta clase es generica (abstracta), las clases que necesiten listas, deben heredar"""
    def __init__(self, node=None):
        self.nodes = []
        self.name="NodeList"
        if node != None:
            self.nodes.append(node)
    def add(self, node):
        self.nodes.append(node)
    def imprimir(self):
        print 'Lista de nodos'
        
class ParamList(NodeList):
    """Una lista de parametros para un metodo: 
    public void setNombre( nombre, apellido)"""
    def __init__(self, node=None):
        NodeList.__init__(self, node)
        self.name = "ParamList"
    def imprimir(self):
        print 'lista de parametros'

class MethList(NodeList):
    """Lista de metodos de una clase"""
    pass

class DeclList(Node): 
    """ Lista las clases 
        Utilizar NodeList (para disminuir la profundidad del arbol 
    """
    def __init__(self, classDecl, declList):
        self.classDecl = classDecl
        self.declList = declList
        self.name="DeclList"
    def imprimir(self):
        print 'lista de declaraciones'
        self.classDecl.imprimir()
        self.declList.imprimir()
        
class DeclListNull(Node): 
    """ Lista null para terminar la recursividad 
        Utilizar NodeList (para disminuir la profundidad del arbol 
    """
    def __init__(self):
        self.name="Null"
        
    def imprimir(self):
        print 'lista de decl null'

class ClassDecl(Node):
    "Un nodo representando una declaracion de una clase."
    def __init__(self, name, fieldDecl, methDecl):
        self.name = name
        self.fieldDecl = fieldDecl
        self.methDecl = methDecl

        
    def imprimir(self):
        print 'declaracion de clase'
        self.fieldDecl.imprimir()
        self.methDecl.imprimir()

class FieldDecl(Node):
    "Nodo que representa la declaracion de atributos de la clase."
    def __init__(self, type, name ):
        self.type=type
        self.name=name
    def imprimir(self):
        print 'declaracion del campo' + self.name
        self.type.imprimir()

class MethDecl(Node):
    "Nodo que representa la declaracion de metodo (sus declaraciones y cuerpo)."
    def __init__(self, type, name, body):
        self.type=type
        self.name=name
        self.body=body        
    def imprimir(self):
        print 'declaracion de metodos: ' + self.name
        self.type.imprimir()
        self.body.imprimir()

class Body(Node):
    "Nodo que representa el cuerpo de un metodo."
    def __init__(self, fieldDecl, statement):
        self.fieldDecl=fieldDecl
        self.statement=statement
        self.name="Body"
    def imprimir(self):
        print 'Cuerpo de la clase'
        self.fieldDecl.imprimir()
        self.statement.imprimir()

class Type(Node):
    """un nodo representando el tipo de otro nodo. Por ejemplo, el
    nodo Binop representando '5 + a', donde a es un integer, tendra 
    un nodo Type asociado con el que representa el hecho que el
    resultado de Binop es un integer. Type puede ser anidado.

    Esta es una clase base abstracta."""

    def __init__(self, child=None):
        if child == None:
            child = NullNode()
        self.child = child

    def set_base_type(self, type):
        """Fija el tipo base (mas interno) de un tipo. Por ejemplo,
        llamando este con un tipo puntero(int) sobre un tipo puntero()
        lo que dara puntero(puntero(int))."""

        if self.child.is_null():
            self.child = type
        else:
            self.child.set_base_type(type)

    def imprimir(self):
        print 'Tipo'

class Expr: pass

class BinOp(Expr):
    def __init__(self,left,op,right):
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op

class Number(Expr):
    def __init__(self,value):
        self.type = "number"
        self.value = value
