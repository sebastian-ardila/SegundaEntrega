class Node():
	def __init__(self,listA, name):
		#numHijos = 0
		self.name = name
		self.listA = listA

	def imprimirPostOrden(self, ident):
	#def imprimirPostOrden(self):

		if type(self.listA) == list:
			numHijos = 0
			while(numHijos <= len(self.listA)-1):
				self.listA[numHijos].imprimirPostOrden("  " +ident)
				#self.listA[numHijos].imprimirPostOrden()
				numHijos = numHijos+1
			#return ident + "Nodo: " + self.name
			print ident + "Nodo: " + self.name

		elif type(self.listA) == unicode:
			print ident + "Nodo: "+ self.name

		elif type(self.listA) == float:
			print ident + "Nodo: "+ self.name

		else:
			self.listA.imprimirPostOrden("\t"+ ident)
			#self.listA.imprimirPostOrden()
			print ident + "Nodo: "+ self.name
		

class ID(Node):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno
    def imprimirPostOrden(self, ident):
        print ident + self.name

class Null(Node):
	def __init__(self):
		self.type = 'void'

	def imprimirPostOrden(self, ident):
		print ident + 'program node null'

 
class empty(Node):
	def __init__(self):
		pass
	#'''empty :'''
	
	