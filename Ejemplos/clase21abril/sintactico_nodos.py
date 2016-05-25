class Nodo():
	#pass

#class A(Nodo):
	#def __init__(self,h1,h2,h3):
		#self.h1=h1
		#self.h2=h2
		#self.h3=h3
		#print("reduce A->(A)")
		
class A(Nodo):
	def __init__(self,listA):
		
		if len(listA) == 3:
			self.listA[1] =listA[1]
			self.listA[2] =listA[2]
			self.listA[3] =listA[3]
			print("reduce A->(A)")
		
		if len(listA) == 1:
			self.listA[1] =listA[1]
			print("reduce A->a")

#class A1(Nodo):
	#def __init__(self, h1):
		#self.h1 = h1
		#print("reduce A->a")
