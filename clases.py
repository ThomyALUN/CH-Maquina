#Esta clase servirá para diferenciar el acumulador de cualquier otro tipo de dato
class Acumulador():

    def __init__(self):
        self.__valor=None

#Esta clase representará el kernel, pero realmente no contendrá nada, solo será para diferenciarla de los demás tipos de datos en la memoria
class Kernel():

    def __init__(self):
        pass

#Esta clase servirá para representar las variables declaradas en el programa
class Variable():

    diccionarioTipos={
        "C": str,
        "I": int,
        "R": float,
        "L": bool
    }

    valorTipos={
        "C": " ",
        "I": 0,
        "R": 0.0,
        "L": False
    }

    def __init__(self, nombre, tipo, valorInicial=None):
        self.__nombre=nombre
        self.__tipo=self.diccionarioTipos[tipo]

        #Se asigna el valor inicial entregado o uno por defecto
        if valorInicial!=None:
            self.__valor=valorInicial
        else:
            self.__valor=self.valorTipos[tipo]