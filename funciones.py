from clases import *

z=1                                                                                 #Último dígito del documento
posAcum=0                                                                           #Por defecto, el acumulador irá en la posición 0
palabrasReservadasCH=[                                                               
'acumulador','cargue','almacene','nueva','lea','sume', 'reste', 'multiplique', 
'divida', 'potencia', 'modulo', 'concatene', 'elimine', 'extraiga', 'Y', 'O',       #Palabras reservadas en el lenguaje CH
'NO', 'muestre', 'imprima', 'retorne', 'vaya', 'vayasi', 'etiqueta', 'logaritmo'
]

def revisarValorInicial(cadena, tipo):

    #Se asume que esta función solo se utiliza cuando se compruebe que el tipo de dato pasado como parámetro es válido dentro del lenguaje CH

    valor=None
    validez=True

    if tipo=="C":
        valor=cadena
    elif tipo=="I":
        try:
            valor=int(cadena)
        except:
            print(f"El valor {cadena} es inválido para el tipo entero.")
            validez=False
    elif tipo=="R":
        try:
            valor=float(cadena)
        except:
            print(f"El valor {cadena} es inválido para el tipo real.")
            validez=False
    else:
        try:
            valor=int(cadena)
            if valor==0 or valor==1:
                pass
            else:
                print(f"El valor {cadena} es inválido para el tipo booleano.")
                validez=False
        except:
            print(f"El valor {cadena} es inválido para el tipo booleano.")
            validez=False

    return validez

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

    #Este diccionario usa como llave los comandos del lenguaje CH y su valor es una lista con la cantidad de argumentos posibles
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
            print(f"Hay un error de sintaxis en la línea {i+1}. No es un comentario o una línea en blanco, y tampoco comienza")
            validez=False
            omitirLineas=None
            break

    return validez, omitirLineas                                   #Se devuelve True o False, según el resultado del chequeo rápido de las líneas

def busquedaEtiquetas(lineasCodigo, omitirLineas, cantidadComandos):

    validez=True
    listaEtiquetas=[]

    for i in range(len(lineasCodigo)):
        if i not in omitirLineas:                                   #Se omiten los comentarios y líneas en blanco
            renglon=lineasCodigo[i]
            comando=renglon[0]
            if comando=="etiqueta":                                 #Se detecta si es una línea que declara una etiqueta
                nombreEtiqueta=renglon[1]
                posicionEtiqueta=renglon[2]
                if nombreEtiqueta in palabrasReservadasCH:          #Se detecta si el nombre de la etiqueta es una palabra reservada del lenguaje CH
                    print(f"{nombreEtiqueta} es una palabra reservada y no puede utilizarse para una etiqueta.")
                    validez=False
                    break
                elif int(posicionEtiqueta)>cantidadComandos:        #Se detecta si la posición para la etiqueta sobrepasa la cantidad de comandos en el archivo
                    print(f"La etiqueta no puede asignarse a la posición {posicionEtiqueta} ya que esta sobrepasa la cantidad.")
                    validez=False
                    break
                else:
                    listaEtiquetas.append(nombreEtiqueta)

    return validez, listaEtiquetas

def revisionEtiquetas(lineasCodigo, omitirLineas, listaEtiquetas):

    validez=True

    for i in range(len(lineasCodigo)):
        if i not in omitirLineas:                               #Se omiten los comentarios y líneas en blanco
            renglon=lineasCodigo[i]
            comando=renglon[0]
            if comando=="vaya":                                 #Se analizan las líneas con comando "vaya" y su etiqueta
                print(f"vaya {renglon[1]}")
                etiqueta=renglon[1]
                if etiqueta not in listaEtiquetas:              #Se detecta si la etiqueta no se encuentra declarada en ninguna parte del código
                    print(f"La etiqueta {etiqueta} no ha sido declarada en el cuerpo del código.")
                    validez=False
                    break
            elif comando=="vayasi":                             #Se analizan las líneas con comando "vayasi" y sus etiquetas
                etiqueta1=renglon[1]
                etiqueta2=renglon[2]
                if (etiqueta1 not in listaEtiquetas):           #Se detecta si la primera etiqueta no se encuentra declarada en ninguna parte del código
                    print(f"La etiqueta {etiqueta1} no ha sido declarada en el cuerpo del código.")
                    validez=False
                    break
                elif (etiqueta2 not in listaEtiquetas):         #Se detecta si la segunda etiqueta no se encuentra declarada en ninguna parte del código
                    print(f"La etiqueta {etiqueta2} no ha sido declarada en el cuerpo del código.")
                    validez=False
                    break

    return validez

def busquedaVariables(lineasCodigo, omitirLineas):

    validez=True
    diccVariables={}    #Este diccionario usa como llave el nombre de la variable y como valor la línea de código donde fue declarada (0 hasta tamaño-1). 

    tiposDeDatos=[
        "C",    #Cadena
        "I",    #Entero
        "R",    #Flotante/Real
        "L",    #Booleano (0-1)
    ]

    for i in range(len(lineasCodigo)):
        if i not in omitirLineas:                                                                                       #Se omiten los comentarios y líneas en blanco
            renglon=lineasCodigo[i]
            comando=renglon[0]
            if comando=="nueva": 
                nombreVariable=renglon[1]
                tipo=renglon[2]

                if nombreVariable in palabrasReservadasCH:                                                              #Se detecta si el nombre de una variable es una palabra reservada del lenguaje CH
                    print(f"El nombre de variable {nombreVariable} es inválido porque es una palabra reservada.")
                    validez=False
                    break
                elif tipo not in tiposDeDatos:                                                                          #Se detecta si el tipo declarado de una variable no existe en el lenguaje CH
                    print(f"El tipo de dato {tipo} no esta soportado en el sistema.")
                    validez=False
                    break
                elif len(renglon)==4 and not revisarValorInicial(renglon[3],tipo):                                      #Se detecta si el valor inicial es válido según el tipo de dato
                    print(f"El valor a asignar como valor inicial {renglon[3]} no es válido para el tipo de dato seleccionado.")
                    validez=False
                    break
                else:
                    diccVariables.update({nombreVariable:i})                                                                #En caso de que la sintaxis este correcta, se almacena el nombre de la variable y la línea de código en que se declaró

    return validez, diccVariables

def revisionVariables(lineasCodigo, omitirLineas, diccVariables):

    validez=True

    #Este diccionario usa como llave los comandos del lenguaje CH y su valor la cantidad de variables posibles en sus argumentos
    comandosCH={
        'cargue':1,
        'almacene':1,
        'lea': 1,
        'sume': 1, 
        'reste': 1, 
        'multiplique': 1, 
        'divida': 1, 
        'potencia': 1, 
        'modulo': 1, 
        'concatene': 1, 
        'elimine': 1, 
        'extraiga': 1, 
        'Y': 3, 
        'O': 3, 
        'NO': 2, 
        'muestre': 1, 
        'imprima': 1, 
        'logaritmo': 1
    }

    for i in range(len(lineasCodigo)):
        if i not in omitirLineas:                                                                                   #Se omiten los comentarios y líneas en blanco
            renglon=lineasCodigo[i]
            comando=renglon[0]
            if comando in comandosCH.keys(): 
                if (comando=="muestre" or comando=="imprima") and renglon[1]=="acumulador":     continue            #Se omiten/dan por válidos los casos en que se muestre o imprima el valor del acumulador
                cantidadVariables=comandosCH[comando]
                for j in range(1,cantidadVariables+1):
                    nombreVariable=renglon[j]                                                          
                    if nombreVariable in palabrasReservadasCH:                                                      #Se detectan las palabras reservadas que han sido utilizadas como nombre de variable
                        print(f"El nombre de {nombreVariable} es inválido porque es una palabra reservada del lenguaje CH.")
                        validez=False
                        break
                    else:
                        lineaDeclaracion=diccVariables.get(nombreVariable,None)
                        if i<lineaDeclaracion or lineaDeclaracion==None:                                            #Se detectan las variables utilizadas antes de su declaración o que son utilizadas sin ser declaradas en ninguna parte del código
                            print(f"La variable {nombreVariable} no fue declarada antes de su uso.")
                            validez=False
                            break
                if not validez: break                                                                               #Se termina la revisión línea por línea si se ha encontrado alguna anomalía en el uso de variables

    return validez


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
    
    print("Primer paso válido\n")
    cantidadComandos=len(lineasCodigo)-len(omitirLineas)            #Se cálcula la cantidad de líneas con comandos hay en el archivo leído 

    validez2, listaEtiquetas=busquedaEtiquetas(lineasCodigo, omitirLineas, cantidadComandos)

    if not validez2:  return False                                  #Si se detecta un error en el segundo paso de la revisión, se termina el chequeo de sintaxis

    print("Segundo paso válido\n")
    print(f"Lista de etiquetas: {listaEtiquetas}\n")
    validez3=revisionEtiquetas(lineasCodigo, omitirLineas, listaEtiquetas)

    if not validez3:  return False                                  #Si se detecta un error en el tercer paso de la revisión, se termina el chequeo de sintaxis

    print("Tercer paso válido\n")
    validez4, diccVariables=busquedaVariables(lineasCodigo, omitirLineas)

    if not validez4: return False                                   #Si se detecta un error en el cuarto paso de la revisión, se termina el chequeo de sintaxis

    print("Cuarto paso válido\n")

    print(f"Lista de variables: {diccVariables}\n")

    validez5=revisionVariables(lineasCodigo, omitirLineas, diccVariables)

    if not validez5: return False                                   #Si se detecta un error en el cuarto paso de la revisión, se termina el chequeo de sintaxis

    print("Quinto paso válido\n")


#main
vectorMemoria=[]
inicializarMemoria(z, posAcum, vectorMemoria)
chequeoSintaxis('programas/factorial.ch')