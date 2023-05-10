# Esta clase servirá para diferenciar el acumulador de cualquier otro tipo de dato
class Acumulador():

    def __init__(self, valor=None, tipo=None):
        self.__valor=valor
        self.__tipo=tipo

    def getTipo(self):
        return self.__tipo
    
    def getValor(self):
        return self.__valor

    def setTipo(self, nuevoTipo):
        self.__tipo=nuevoTipo
    
    def setValor(self, nuevoValor):
        self.__valor=nuevoValor

    def copia(self):
        copia=Acumulador(self.__valor, self.__tipo)
        return copia

# Esta clase representará el kernel, pero realmente no contendrá nada, 
# solo será para diferenciarla de los demás tipos de datos en la memoria
class Kernel():

    def __init__(self):
        pass

# Esta clase servirá para representar las variables declaradas en el programa
class Variable():

    valorTipos={
        "C": " ",
        "I": 0,
        "R": 0.0,
        "L": 0
    }

    def __init__(self, nombre, tipo, valorInicial=None):
        self.__nombre=nombre
        self.__tipo=tipo

        #Se asigna el valor inicial entregado o uno por defecto
        if valorInicial!=None:
            self.__valor=valorInicial
        else:
            self.__valor=self.valorTipos[tipo]

    def getNombre(self):
        return self.__nombre
    
    def getTipo(self):
        return self.__tipo
    
    def getValor(self):
        return self.__valor
    
    def setValor(self,nuevoValor):
        self.__valor=nuevoValor

class Programa:
    proxConsecutivo=0
    tiempoLlegada=0
    def __init__(self, ruta:str, limitesPrograma:list, posVariablesMem:dict, diccEtiquetas:dict):
        self.id=Programa.proxConsecutivo
        self.nombre=ruta.split("\\")[-1]
        self.espIns=limitesPrograma[1]-limitesPrograma[0]-1
        self.espMem=self.espIns+len(posVariablesMem)+len(diccEtiquetas)
        self.insAct=limitesPrograma[0]
        self.prioridad=None
        self.qRest=0
        self.llegada=Programa.tiempoLlegada
        self.tiempoRest=None

        self.limites=limitesPrograma
        self.posVariablesMem=posVariablesMem
        self.diccEtiquetas=diccEtiquetas

        self.terminado=False
        self.estadoAcum=Acumulador()

        Programa.proxConsecutivo+=1
        Programa.tiempoLlegada+=(limitesPrograma[1]-limitesPrograma[0])*4

    def cambiarIns(self, nextIns:int):
        if nextIns>self.limites[1]:
            nextIns=self.limites[1]
        else:
            self.insAct=nextIns
    
    def cambiarPrioridad(self, prioridad:int):
        self.prioridad=prioridad

    def terminarPrograma(self):
        self.terminado=True

    def almacenarAcum(self, obj:Acumulador):
        self.estadoAcum=obj.copia()

    def resetClase():
        Programa.proxConsecutivo=0
        Programa.tiempoLlegada=0