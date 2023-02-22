from clases import *
from math import log10, ceil

z=1                                                                                 #Último dígito del documento
posAcum=0                                                                           #Por defecto, el acumulador irá en la posición 0
palabrasReservadasCH=['acumulador']                                                 #Palabras reservadas en el lenguaje CH 

#Se exporta todo lo que hay en la memoria en un archivo .txt
def guardarMemoriaTXT(vectorMemoria):
    archivo=open("memoria.txt","w")
    for i in range(len(vectorMemoria)):
        linea=vectorMemoria[i]
        pos=i
        cadena=f"{agregarCeros(pos,4)}"
        if type(linea)==Acumulador:
            cadena=f"{cadena}\tAcumulador\n"
        elif type(linea)==Kernel:
            cadena=f"{cadena}\tKernel\n"
        elif type(linea)==Variable:
            cadena=f"{cadena}\t{linea.getValor()}\n"
        else:
            cadena=f"{cadena}\t{linea}\n"
        archivo.write(cadena)
    archivo.close()

#Se exporta la ubicación y el valor de las variables en un archivo .txt
def guardarVariablesTXT(vectorMemoria, posVariablesMem):
    archivo=open("variables.txt","w")
    cadena="Pos \tVariables\tValores\n"
    archivo.write(cadena)
    for variable, pos in posVariablesMem.items():
        cadena=f"{agregarCeros(pos,4)}\t{variable}\t{vectorMemoria[pos].getValor()}\n"
        archivo.write(cadena)
    archivo.close()

#Se exporta la dirección de apuntado y nombre de las etiquetas
def guardarEtiquetasTXT(diccEtiquetas):
    archivo=open("etiquetas.txt","w")
    cadena="Pos \tEtiquetas\n"
    archivo.write(cadena)
    for etiqueta, pos in diccEtiquetas.items():
        cadena=f"{agregarCeros(pos,4)}\t{etiqueta}\n"
        archivo.write(cadena)
    archivo.close()

#Se exporta el valor de una variable a la impresora
def imprima(valor):
    cadena=f"RESULTADO: {valor}"
    with open("impresora.txt","w") as archivo:
        archivo.write(cadena)

#Se exporta el valor de una variable a la pantalla
def muestre(valor):
    cadena=f"RESULTADO: {valor}"
    with open("pantalla.txt","w") as archivo:
        archivo.write(cadena)

#Se agregan 0's para dar formato a la posición de memoria mostrada al usuario
def agregarCeros(pos, ceros):
    if pos!=0:
        cifras=ceil(log10(pos))
    else:
        cifras=1
    diferencia=ceros-cifras
    numFormateado=""

    if potencia10(pos) or pos==1:
        diferencia-=1
    
    for i in range(diferencia):
        numFormateado+="0"
    numFormateado+=str(pos)
    return numFormateado

#Se calcula si un número es potencia de 10
def potencia10(num):
    potencia=False
    while num>=10:
        num=num/10
        if num==1:
            potencia=True
    return potencia

def ejecutarPaso(apuntador, vectorMemoria, diccEtiquetas, posVariablesMem, omitirLineasGlobal):
    valido=True                             #Se asume que el funcionamiento es correcto
    fin=False                               #Se asume que la línea no es de retorno
    linea=vectorMemoria[apuntador]
    tipoDato=type(vectorMemoria[apuntador])
    aritmeticos=["sume", "reste", "multiplique", "divida", "potencia", "modulo"]
    proxDirecc=apuntador+1
    if apuntador not in omitirLineasGlobal and tipoDato!=Variable and linea!=None:
        linea=linea.split()
        comando=linea[0]
        print(f"{apuntador}:{linea}",end="")
        if comando=="nueva" or comando=="etiqueta":
            print(f" :Línea ignorada", end="")
        elif comando=="cargue":
            #Se traen los datos de la variable a cargar al acumulador
            variable=linea[1]
            posVar=posVariablesMem[variable]
            objetoVar=vectorMemoria[posVar]
            valor=objetoVar.getValor()
            tipo=objetoVar.getTipo()

            #Se suben los datos al acumulador
            objetoAcum=vectorMemoria[0]
            objetoAcum.setTipo(tipo)
            objetoAcum.setValor(valor)
            vectorMemoria[0]=objetoAcum
            
            #print(f": Variable a cargar {variable}:{posVar}:{vectorMemoria[posVar]}:Valor={valor}:Tipo={tipo}")
        elif comando=="almacene":
            #Se cargan los datos de la variable a sobreescribir
            variable=linea[1]
            posVar=posVariablesMem[variable]
            objetoVar=vectorMemoria[posVar]
            tipoVar=objetoVar.getTipo()

            #Se obtiene el tipo de dato del acumulador
            objetoAcum=vectorMemoria[0]
            tipoAcum=objetoAcum.getTipo()

            if tipoVar==tipoAcum:               #Se comprueba que el tipo de dato del acumulador es el mismo que el tipo de dato de la variable
                valorAcum=objetoAcum.getValor()
                objetoVar.setValor(valorAcum)
                vectorMemoria[posVar]=objetoVar
            elif tipoVar=="I" and tipoAcum=="R":
                valorAcum=objetoAcum.getValor()
                objetoVar.setValor(int(valorAcum))
                vectorMemoria[posVar]=objetoVar
            else:
                print(f"\nTipo de dato inválido {tipoVar} y {tipoAcum} no son equivalentes.")
                valido=False
        
        elif comando in aritmeticos:
            variable=linea[1]
            posVar=posVariablesMem[variable]
            objetoVar=vectorMemoria[posVar]
            tipoVar=objetoVar.getTipo()
            if tipoVar!="I" and tipoVar!="R":
                print(f"La variable {variable} no tiene el tipo de dato entero o real, por lo tanto no se puede realizar la operación.")
                valido=False
            else:
                valorVar=objetoVar.getValor()
                objetoAcum=vectorMemoria[0]
                tipoAcum=objetoAcum.getTipo()
                if tipoAcum!="I" and tipoAcum!="R":
                    print(f"El acumulador no tiene el tipo de dato entero o real, por lo tanto no se puede realizar la operación.")
                    valido=False
                else:
                    valorAcum=objetoAcum.getValor()
                    if comando=="sume": 
                        valorAcum+=valorVar
                    elif comando=="reste": 
                        valorAcum-=valorVar
                    elif comando=="multiplique": 
                        valorAcum*=valorVar
                    else:
                        if (comando=="divida" or comando=="modulo") and valorVar==0: 
                            print(f"El valor del divisor es 0. El programa no puede continuar.")
                            valido=False
                        elif comando=="divida":
                            valorAcum/=valorVar
                        elif comando=="modulo":
                            valorAcum%=valorVar
                        elif comando=="potencia" and tipoVar=="I": 
                            valorAcum=pow(valorAcum, valorVar)
                        else:
                            print(f"El valor del exponente no es entero ({valorVar}). El programa no puede continuar.")
                            valido=False

                    if valido:
                        objetoAcum.setValor(valorAcum)
                        vectorMemoria[0]=objetoAcum
        
        elif comando=="vaya":
            etiqueta=linea[1]
            proxDirecc=diccEtiquetas[etiqueta]
        elif comando=="vayasi":
            objetoAcum=vectorMemoria[0]
            tipoAcum=objetoAcum.getTipo()
            if tipoAcum=="C":
                print(f"No es posible continuar con el programa. El valor del acumulador no es númerico y no permite tomar una decisión.")
            else:
                valorAcum=objetoAcum.getValor()
                if valorAcum>0:
                    etiqueta1=linea[1]
                    proxDirecc=diccEtiquetas[etiqueta1]
                elif valorAcum<0:
                    etiqueta2=linea[2]
                    proxDirecc=diccEtiquetas[etiqueta2]
        elif comando=="muestre":
            variable=linea[1]
            if variable!="acumulador":
                posVar=posVariablesMem[variable]
                objeto=vectorMemoria[posVar]
            else:
                objeto=vectorMemoria[0]
            valor=objeto.getValor()
            muestre(valor)
        elif comando=="imprima":
            variable=linea[1]
            if variable!="acumulador":
                posVar=posVariablesMem[variable]
                objeto=vectorMemoria[posVar]
            else:
                objeto=vectorMemoria[0]
            valor=objeto.getValor()
            imprima(valor)
        elif comando=="retorne":
            fin=True
    else:   #Se detectan los comentarios o líneas en blanco
        print(f"{apuntador}: Linea omitida",end="")

    print("")
    if not valido:
        return valido

    print(vectorMemoria[0].getValor(), vectorMemoria[0].getTipo())
    guardarMemoriaTXT(vectorMemoria)
    guardarVariablesTXT(vectorMemoria, posVariablesMem)

    apuntador=proxDirecc
    return apuntador, valido, fin

def ejecutarTodo(apuntador, vectorMemoria, diccEtiquetas, posVariablesMem, omitirLineasGlobal):
    while True:
        tupla=ejecutarPaso(apuntador, vectorMemoria, diccEtiquetas, posVariablesMem, omitirLineasGlobal)
        if len(tupla)>1:
            apuntador, valido, fin=tupla
        else: break

        if fin or apuntador>=len(vectorMemoria):
            break

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

def inicializarMemoria(z, posAcum):
    sizeKernel=z*10+9
    sizeMemoria=z*10+50
    vectorMemoria=[None for i in range(sizeMemoria)]    #Por convención, el tipo de dato None representará espacios de memoria vacíos

    vectorMemoria[posAcum]=Acumulador()                 #El acumulador toma un valor arbitrario para diferenciarlo del resto de espacios de memoria

    #Se llenan los siguientes espacios de memoria con el kernel
    kernelVacio=Kernel()
    for i in range(1,(sizeKernel+1)):
        vectorMemoria[i]=kernelVacio

    posDispMem=sizeKernel+1                             #Se calcula la posición de memoria desde la cual hay espacios libres
    return vectorMemoria, posDispMem

def revisionRapida(lineasCodigo):

    validez=True                    #Inicialmente se asume que el código no tiene errores
    omitirLineas=[]
    posRetorne=None

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
        'vaya': [2], 
        'vayasi': [3], 
        'etiqueta': [3], 
        'logaritmo': [2]
    }
    
    for i in range(len(lineasCodigo)):
        renglon=lineasCodigo[i]
        if renglon==[]:                                                                 #Este condicional detecta las líneas en blanco
            omitirLineas.append(i)
        elif renglon[0][0:2]=="//":                                                     #Este condicional detecta los comentarios
            omitirLineas.append(i)
        elif renglon[0]=="retorne" and (len(renglon)==1 or len(renglon)==2):            #Este condicional detecta la línea en que se encuentra el retorne
            posRetorne=i
            break
        elif renglon[0] in comandosCH.keys():                                           #Este condicional detecta si la primera palabra de la línea de código es alguno de los comandosCH
            llave=renglon[0]
            sizeRenglon=len(renglon)                                                    #Acá de cálcula la cantidad de palabras en la línea de código
            sizeComando=comandosCH[llave]                                               #Acá se revisa la cantidad de palabras que puede/debe tener la línea de código según el comando
            if sizeRenglon not in sizeComando:                                          #Se detecta si la cantidad en la línea no es válida
                print(f"La longitud de la línea {i+1} es inválida.")
                validez=False
                omitirLineas=None
                break
        else:                                                                           #En este caso, se detecta que hay una línea que no es un comentario, una línea en blanco o un comandoCH por lo que hay un error de sintaxis y se actualiza el valor booleano
            print(f"Hay un error de sintaxis en la línea {i+1}. No es un comentario o una línea en blanco, y tampoco comienza con un comando.")
            validez=False
            omitirLineas=None
            break

    if posRetorne:
        return validez, omitirLineas, posRetorne                                        #Se devuelve True o False, según el resultado del chequeo rápido de las líneas, la posición de las líneas en blanco y líneas de comentarios, y la posición donde se encontro la primera sentencia retorne
    else:
        return False, None, None

def busquedaEtiquetas(lineasCodigo, omitirLineas, posRetorne, cantidadComandos):

    validez=True
    diccEtiquetas={}

    for i in range(posRetorne):                                     #Se llega hasta antes de la sentencia retorne
        if i not in omitirLineas:                                   #Se omiten los comentarios y líneas en blanco
            renglon=lineasCodigo[i]
            comando=renglon[0]
            if comando=="etiqueta":                                 #Se detecta si es una línea que declara una etiqueta
                nombreEtiqueta=renglon[1]
                posicionEtiqueta=int(renglon[2])
                if nombreEtiqueta in palabrasReservadasCH:          #Se detecta si el nombre de la etiqueta es una palabra reservada del lenguaje CH
                    print(f"{nombreEtiqueta} es una palabra reservada y no puede utilizarse para una etiqueta.")
                    validez=False
                    break
                elif posicionEtiqueta>cantidadComandos:        #Se detecta si la posición para la etiqueta sobrepasa la cantidad de comandos en el archivo
                    print(f"La etiqueta no puede asignarse a la posición {posicionEtiqueta} ya que esta sobrepasa la cantidad.")
                    validez=False
                    break
                else:
                    lineaEtiqueta=0                                 #Se calcula la línea de código a la cual debe apuntar la etiqueta(linea etiqueta cuenta de 1 a n, mientras los indices del SO van de 0 a n-1)
                    for j in range(posRetorne+1):
                        if j not in omitirLineas:
                            lineaEtiqueta+=1
                        if lineaEtiqueta==posicionEtiqueta:
                            break
                    diccEtiquetas.update({nombreEtiqueta:j})        #Se genera un diccionario con el nombre de la etiqueta como la clave y la linea de código a la que apunta como el valor

    return validez, diccEtiquetas

def revisionEtiquetas(lineasCodigo, omitirLineas, posRetorne, diccEtiquetas):

    validez=True

    for i in range(posRetorne):                                 #Se llega hasta antes de la sentencia retorne
        if i not in omitirLineas:                               #Se omiten los comentarios y líneas en blanco
            renglon=lineasCodigo[i]
            comando=renglon[0]
            if comando=="vaya":                                 #Se analizan las líneas con comando "vaya" y su etiqueta
                print(f"vaya {renglon[1]}")
                etiqueta=renglon[1]
                if etiqueta not in diccEtiquetas:              #Se detecta si la etiqueta no se encuentra declarada en ninguna parte del código
                    print(f"La etiqueta {etiqueta} no ha sido declarada en el cuerpo del código.")
                    validez=False
                    break
            elif comando=="vayasi":                             #Se analizan las líneas con comando "vayasi" y sus etiquetas
                etiqueta1=renglon[1]
                etiqueta2=renglon[2]
                if (etiqueta1 not in diccEtiquetas):           #Se detecta si la primera etiqueta no se encuentra declarada en ninguna parte del código
                    print(f"La etiqueta {etiqueta1} no ha sido declarada en el cuerpo del código.")
                    validez=False
                    break
                elif (etiqueta2 not in diccEtiquetas):         #Se detecta si la segunda etiqueta no se encuentra declarada en ninguna parte del código
                    print(f"La etiqueta {etiqueta2} no ha sido declarada en el cuerpo del código.")
                    validez=False
                    break

    return validez

def busquedaVariables(lineasCodigo, omitirLineas, posRetorne):

    validez=True
    diccVariables={}    #Este diccionario usa como llave el nombre de la variable y como valor la línea de código donde fue declarada (0 hasta tamaño-1). 

    tiposDeDatos=[
        "C",    #Cadena
        "I",    #Entero
        "R",    #Flotante/Real
        "L",    #Booleano (0-1)
    ]

    for i in range(posRetorne):                                     #Se llega hasta antes de la sentencia retorne
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
                elif len(nombreVariable)>255:                                                                           #Se detecta si el nombre de una variable tiene más de 255 caracteres
                    print(f"El nombre de variable {nombreVariable} excede la longitud máxima.")
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
                    if len(renglon)==3:
                        valorInicial=None
                    else:
                        valorInicial=renglon[3]
                        if tipo=="I" or tipo=="L": valorInicial=int(valorInicial)
                        elif tipo=="R": valorInicial=float(valorInicial)
                    diccVariables.update({nombreVariable:[i, tipo, valorInicial]})                                                                #En caso de que la sintaxis este correcta, se almacena el nombre de la variable y la línea de código en que se declaró

    return validez, diccVariables

def revisionVariables(lineasCodigo, omitirLineas, posRetorne, diccVariables):

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

    for i in range(posRetorne):                                                                                     #Se llega hasta antes de la sentencia retorne
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
                        if type(lineaDeclaracion)==list:
                            lineaDeclaracion=lineaDeclaracion[0]
                        if lineaDeclaracion==None or i<lineaDeclaracion:                                            #Se detectan las variables utilizadas antes de su declaración o que son utilizadas sin ser declaradas en ninguna parte del código
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

    validez1, omitirLineas, posRetorne=revisionRapida(lineasCodigo)

    if not validez1:  return False                           #Si se detecta un error en el primer paso de la revisión, se termina el chequeo de sintaxis
    
    print("Primer paso válido\n")
    cantidadComandos=len(lineasCodigo)-len(omitirLineas)            #Se cálcula la cantidad de líneas con comandos hay en el archivo leído 

    validez2, diccEtiquetas=busquedaEtiquetas(lineasCodigo, omitirLineas, posRetorne, cantidadComandos)

    if not validez2:  return False                           #Si se detecta un error en el segundo paso de la revisión, se termina el chequeo de sintaxis

    print("Segundo paso válido\n")
    print(f"Lista de etiquetas: {diccEtiquetas}\n")
    validez3=revisionEtiquetas(lineasCodigo, omitirLineas, posRetorne, diccEtiquetas)

    if not validez3:  return False                           #Si se detecta un error en el tercer paso de la revisión, se termina el chequeo de sintaxis

    print("Tercer paso válido\n")
    validez4, diccVariables=busquedaVariables(lineasCodigo, omitirLineas, posRetorne)

    if not validez4: return False                            #Si se detecta un error en el cuarto paso de la revisión, se termina el chequeo de sintaxis

    print("Cuarto paso válido\n")

    print(f"Lista de variables: {diccVariables}\n")

    validez5=revisionVariables(lineasCodigo, omitirLineas, posRetorne, diccVariables)

    if not validez5: return False                            #Si se detecta un error en el cuarto paso de la revisión, se termina el chequeo de sintaxis

    print("Quinto paso válido\n")

    celdasMemNecesarias=posRetorne+len(diccEtiquetas)+len(diccVariables.keys())
    return True, celdasMemNecesarias, posRetorne, diccEtiquetas, diccVariables, omitirLineas

def cargarPrograma(ruta, posDispMem, vectorMemoria, omitirLineasGlobal):

    tupla=chequeoSintaxis(ruta)
    if len(tupla)>1:
        sintaxisValida, celdasMemNecesarias, posRetorne, diccEtiquetas, diccVariables, omitirLineas=tupla
    else:
        sintaxisValida=tupla

    omitirLineasGlobal=omitirLineasGlobal+[num+posDispMem for num in omitirLineas]

    if not sintaxisValida: 
        print("La sintaxis del programa tiene errores.")
        return False

    with open(ruta,'r') as archivo:                         #Se vuelve a leer el archivo línea por línea
        lineasCodigo=archivo.readlines()

    for i in range(len(lineasCodigo)):                      #En este caso, solo se quitan los saltos de línea de cada renglon leído
        lineasCodigo[i]=lineasCodigo[i].rstrip()
    
    if (len(vectorMemoria)-(posDispMem))<celdasMemNecesarias:
        print("No hay suficiente espacio en memoria.")
        return False

    for i in range(posRetorne+1):               #Se cargan en memoria las líneas de código halladas antes del retorne
        vectorMemoria[i+posDispMem]=lineasCodigo[i]
    
    for key in diccEtiquetas.keys():            #Se ubican correctamente las direcciones las que apuntan las etiquetas
        diccEtiquetas[key]=diccEtiquetas[key]+posDispMem 

    posDispMem=posDispMem+posRetorne+1          #Nueva ubicación de las posiciones de memoria disponibles

    listaVariables=[]                           #Se crea una lista con objetos de tipo variable que serán cargados en la memoria
    for key, value in diccVariables.items():
        nombreVariable=key
        datosVariable=value
        tipo=datosVariable[1]
        valorInicial=datosVariable[2]
        variableMemoria=Variable(nombreVariable, tipo, valorInicial)
        listaVariables.append(variableMemoria)

    posVariablesMem={}                          #Se almacena el nombre de las variables usadas por el programa y su dirección de memoria
    for i in range(len(listaVariables)):
        nombreVariable=listaVariables[i].getNombre()
        vectorMemoria[i+posDispMem]=listaVariables[i]
        posVariablesMem.update({nombreVariable:i+posDispMem})
        omitirLineasGlobal.append(i+posDispMem)

    posDispMem=posDispMem+len(listaVariables)         #Nueva ubicación de las posiciones de memoria disponibles

    guardarEtiquetasTXT(diccEtiquetas)
    guardarVariablesTXT(vectorMemoria, posVariablesMem)
    guardarMemoriaTXT(vectorMemoria)
    
    return True, vectorMemoria, diccEtiquetas, posVariablesMem, posDispMem, omitirLineasGlobal

#main
omitirLineasGlobal=[]
vectorMemoria, posDispMem=inicializarMemoria(z, posAcum)
apuntador=posDispMem   #Esta variable apunta a la próxima instrucción a ser ejecutada
print("***"*5+"INICIO PROGRAMA"+"***"*5+"\n")
print(f"Inicialización memoria: {vectorMemoria}")
print(f"\nLuego de separar espacio para el acumulador y el kernel, hay espacio dispinible desde la posición {posDispMem}.\n")
tupla=cargarPrograma('programas/factorial.ch', posDispMem, vectorMemoria, omitirLineasGlobal)
if len(tupla)>1:
    valido, vectorMemoria, diccEtiquetas, posVariablesMem, posDispMem, omitirLineasGlobal=tupla
else:
    valido=False

print(diccEtiquetas)
print(posVariablesMem)

if not valido:
    print("El programa no puede ejecutarse")
    exit()

ejecutarTodo(apuntador, vectorMemoria, diccEtiquetas, posVariablesMem, omitirLineasGlobal)

"""while True:
        input("Presione enter para ejecutar la siguiente instrucción...")
        tupla=ejecutarPaso(apuntador, vectorMemoria, diccEtiquetas, posVariablesMem, omitirLineasGlobal)
        if len(tupla)>1:
            apuntador, valido, fin=tupla
        else: break

        if fin or apuntador>=len(vectorMemoria):
            break"""
