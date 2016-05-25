class Nodo:
    pass

class ExpSuma(Nodo):
    def __init__(self, op1, op2):
        self.op1=op1
        self.op2=op2
    def preorden(self):
        print 'E+'
        self.op1.preorden()
        self.op2.preorden()
        
    #def postorden(self):

    #def evaluar():
        #self.res=self.op1.evaluar()+ self.op2.evaluar()
        #return self.res
                
        
class ExpMult(Nodo):
    def __init__(self, op1, op2):
        self.op1=op1
        self.op2=op2
    def preorden(self):
        print 'E*'
        self.op1.preorden()
        self.op2.preorden()

class ExpNumero(Nodo):
    def __init__(self, valor):
        self.valor=valor
        
    def preorden(self):
        print self.valor

    
