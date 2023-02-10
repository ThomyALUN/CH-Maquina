from clases import *

z=1 #Último dígito del documento
posAcum=0 #Por defecto, el acumulador irá en la posición 0

def inicializarMemoria(z, posAcum, vectorMemoria):
    sizeKernel=z*10+9
    sizeMemoria=z*10+50
    vectorMemoria=[None for i in range(sizeMemoria)] #Por convención, el tipo de dato None representará espacios de memoria vacíos

    vectorMemoria[posAcum]=Acumulador() #El acumulador toma un valor arbitrario para diferenciarlo del resto de espacios de memoria

    #Se llenan los siguientes espacios de memoria con el kernel
    kernelVacio=Kernel()
    for i in range(1,(sizeKernel+1)):
        vectorMemoria[i]=kernelVacio

    # print(f'El valor de z es {z}, el tamaño del kernel es de {sizeKernel} y el tamaño inicial de memoria es de {sizeMemoria}.')
    # print(vectorMemoria)

def instruccionValida(linea):
    instruccionCorrecta=True
    partesOperacion=linea.split() #Se separan las palabras/parametros que hacen parte de la instrucción
    pass

def chequeoSintaxis(ruta):
    sintaxisValida=True

    #Se lee el archivo
    with open(ruta,'r') as archivo:
        datos=archivo.readlines()

    for renglon in datos:
        linea=renglon.strip() #Con esto se quitan los espacios en blanco y saltos de línea a izquierda y derecha del texto

    return sintaxisValida

#main
if __name__=="main":
    vectorMemoria=[]
    inicializarMemoria(z, posAcum, vectorMemoria)
    chequeoSintaxis('programas/factorial.ch')