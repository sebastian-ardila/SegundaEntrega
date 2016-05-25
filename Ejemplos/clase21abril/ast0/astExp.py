class Nodo:
    pass

class ExpSuma(Nodo):
    def __init__(self, op1, op2):
        self.op1=op1
        self.op2=op2
    def calcular(self):
        return self.op1.calcular()+self.op2.calcular()
        
class ExpMult(Nodo):
    def __init__(self, op1, op2):
        self.op1=op1
        self.op2=op2
    def calcular(self):
        return self.op1.calcular()*self.op2.calcular()

class ExpNumero(Nodo):
    def __init__(self, valor):
        self.valor=valor
        print valor
    def calcular(self):
        return self.valor

    
