from clases import *

z=1                                                                                 #Último dígito del documento
posAcum=0                                                                           #Por defecto, el acumulador irá en la posición 0
palabrasReservadasCH=[                                                               
'acumulador','cargue','almacene','nueva','lea','sume', 'reste', 'multiplique', 
'divida', 'potencia', 'modulo', 'concatene', 'elimine', 'extraiga', 'Y', 'O',       #Palabras reservadas en el lenguaje CH
'NO', 'muestre', 'imprima', 'retorne', 'vaya', 'vayasi', 'etiqueta', 'logaritmo'
]

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

def revisionRapida(lineasCodigo):

    validez=True                    #Inicialmente se asume que el código no tiene errores
    omitirLineas=[]

    comandosCH={
        'cargue':[2],
        'almacene':[2],
        'nueva':[3,4],
        'lea': [2],
        'sume': [2], 
        'reste': [2], 
        'multiplique': [2], 
        'divida': [2], 
        'potencia': [2], 
        'modulo': [2], 
        'concatene': [2], 
        'elimine': [2], 
        'extraiga': [2], 
        'Y': [4], 
        'O': [4], 
        'NO': [3], 
        'muestre': [2], 
        'imprima': [2], 
        'retorne': [1,2], 
        'vaya': [2], 
        'vayasi': [3], 
        'etiqueta': [3], 
        'logaritmo': [2]
    }
    
    for i in range(len(lineasCodigo)):
        renglon=lineasCodigo[i]
        if renglon==[]:                                 #Este condicional detecta las líneas en blanco
            omitirLineas.append(i)
        elif renglon[0][0:2]=="//":                     #Este condicional detecta los comentarios
            omitirLineas.append(i)
        elif renglon[0] in comandosCH.keys():           #Este condicional detecta si la primera palabra de la línea de código es alguno de los comandosCH
            llave=renglon[0]
            sizeRenglon=len(renglon)                        #Acá de cálcula la cantidad de palabras en la línea de código
            sizeComando=comandosCH[llave]                   #Acá se revisa la cantidad de palabras que puede/debe tener la línea de código según el comando
            if sizeRenglon not in sizeComando:              #Se detecta si la cantidad en la línea no es válida
                print(f"La longitud de la línea {i+1} es inválida.")
                validez=False
                omitirLineas=None
                break
        else:                                           #En este caso, se detecta que hay una línea que no es un comentario, una línea en blanco o un comandoCH por lo que hay un error de sintaxis y se actualiza el valor booleano
            print(f"Hay un error de sintaxis en la línea {i+1}.")
            validez=False
            omitirLineas=None
            break

    return validez, omitirLineas                                   #Se devuelve True o False, según el resultado del chequeo rápido de las líneas

def busquedaEtiquetas(lineasCodigo, omitirLineas, cantidadComandos):

    validez=True
    listaEtiquetas=[]

    for i in range(len(lineasCodigo)):
        if i not in omitirLineas:                               #Se omiten los comentarios y líneas en blanco
            renglon=lineasCodigo[i]
            comando=renglon[0]
            if comando=="etiqueta":                             #Se detecta si es una línea que declara una etiqueta
                nombreEtiqueta=renglon[1]
                posicionEtiqueta=renglon[2]
                if nombreEtiqueta in palabrasReservadasCH:      #Se detecta si el nombre de la etiqueta es una palabra reservada del lenguaje CH
                    validez=False
                elif posicionEtiqueta>cantidadComandos:         #Se detecta si la posición para la etiqueta sobrepasa la cantidad de comandos en el archivo
                    validez=False
                else:
                    listaEtiquetas.append(nombreEtiqueta)

    return validez, listaEtiquetas

def chequeoSintaxis(ruta):

    #Se lee el archivo
    with open(ruta,'r') as archivo:
        lineasCodigo=archivo.readlines()

    for i in range(len(lineasCodigo)):
        lineasCodigo[i]=lineasCodigo[i].strip() #Con esto se quitan los espacios en blanco y saltos de línea a izquierda y derecha del texto
        lineasCodigo[i]=lineasCodigo[i].split() #Con esto se separan las palabras de la cadena de texto
    print(lineasCodigo,"\n")

    validez1, omitirLineas=revisionRapida(lineasCodigo)

    if not validez1:  return False                                  #Si se detecta un error en el primer paso de la revisión, se termina el chequeo de sintaxis
    
    cantidadComandos=len(lineasCodigo)-len(omitirLineas)            #Se cálcula la cantidad de líneas con comandos hay en el archivo leído 

    validez2, listaEtiquetas=busquedaEtiquetas(lineasCodigo, omitirLineas, cantidadComandos)

    if not validez2:  return False                                  #Si se detecta un error en el primer paso de la revisión, se termina el chequeo de sintaxis




#main
vectorMemoria=[]
inicializarMemoria(z, posAcum, vectorMemoria)
chequeoSintaxis('programas/factorial.ch')