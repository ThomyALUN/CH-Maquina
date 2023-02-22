#Esta clase servirá para diferenciar el acumulador de cualquier otro tipo de dato
class Acumulador():

    def __init__(self):
        self.__valor=None
        self.__tipo=None

    def getTipo(self):
        return self.__tipo
    
    def getValor(self):
        return self.__valor

    def setTipo(self, nuevoTipo):
        self.__tipo=nuevoTipo
    
    def setValor(self, nuevoValor):
        self.__valor=nuevoValor

#Esta clase representará el kernel, pero realmente no contendrá nada, solo será para diferenciarla de los demás tipos de datos en la memoria
class Kernel():

    def __init__(self):
        pass

#Esta clase servirá para representar las variables declaradas en el programa
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