from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from math import log

from ventanasDisenos.explorador import *
from ventanasDisenos.secciones import *
from ventanasDisenos.lecturaValor import *
from ventanasDisenos.mensajeError import *


class VentanaPrincipal(GridLayout):
    algoritmos=["FCFS","SJF","SRTN","Prioridad no expropiativo","Prioridad expropiativo","Round Robin","Round Robin con Prioridad"]
    def __init__(self, appPpal, **kwargs):
        self.rows=4
        super(VentanaPrincipal, self).__init__(**kwargs)
        self.quantum=None
        self.appPpal=appPpal
        self.ventanaInicial()

    def ventanaInicial(self, obj=None):
        Window.clearcolor=(26/255, 78/255, 82/255, 0.8)
        Window.size=(650,600)
        Window.top=540-Window.height/2
        Window.left=960-Window.width/2
        self.clear_widgets()
        self.finDocumento=1
        self.sizeKernel=self.finDocumento*10+9
        self.sizeMemoria=self.finDocumento*10+100

        tituloPpal=Label(text="[b]Bienvenido al CH-MÁQUINA[/b]", markup=True, size_hint_y=0.2, height=100, font_size="40sp")
        indicacion=Label(text="Ingrese los siguientes datos antes de continuar", markup=True, size_hint_y=0.1, height=100, font_size="20sp")
        self.setConfiguraciones=SeccionTamanio(self, size_hint_y=0.58)

        areaBotones=BoxLayout(orientation="horizontal", padding=[80,10], size_hint_y=0.12, spacing=70)

        botonAceptar=Button(text="Aceptar")
        botonAceptar.bind(on_release=self.aceptarSize)
        botonCerrar=Button(text="Cerrar programa")
        botonCerrar.bind(on_release=self.cerrar)

        areaBotones.add_widget(botonAceptar)
        areaBotones.add_widget(botonCerrar)

        self.add_widget(tituloPpal)
        self.add_widget(indicacion)
        self.add_widget(self.setConfiguraciones)
        self.add_widget(areaBotones)


    def aceptarSize(self, obj):
        self.sizeKernel=int(self.setConfiguraciones.inputKernel.text)
        self.sizeMemoria=int(self.setConfiguraciones.inputMemoria.text)
        self.algoritmo=self.setConfiguraciones.pedirAlg.botonPpal.text
        if self.sizeKernel>=self.sizeMemoria:
            self.abrirError("El tamaño del Kernel debe ser menor que el tamaño de la memoria", (0.7, 0.7))
        elif self.algoritmo==PedirTamanio.algoritmos[0]:
            self.abrirError("No ha seleccionado ningún algoritmo de planificación", (0.7, 0.7))
        else:
            self.indAlg=self.algoritmos.index(self.algoritmo)
            self.iniciarCH()

    def cerrar(self, obj):
        self.appPpal.stop()

    def cargarAlgoritmo(self):
        # ["FCFS","SJF","SRTN","Prioridad no expropiativo","Prioridad expropiativo","Round Robin","Round Robin con Prioridad"]
        if self.indAlg==0:
            # FCFS
            programa=self.listaProgramas[self.programaLeido]
            programa.cambiarPrioridad(100-programa.id)
        elif self.indAlg==1:
            # SJF (No expropiativo)
            pass
        elif self.indAlg==2:
            # SJF (Expropiativo)
            pass
        elif self.indAlg==3:
            # Prioridad no expropiativo
            self.abrirLecPrioridad()
        elif self.indAlg==4:
            # Prioridad expropiativo
            self.abrirLecPrioridad()
        elif self.indAlg==5:
            # Round Robin
            pass
        else:
            # Round Robin con prioridad
            self.abrirLecPrioridad()

    def pasoAlgoritmo(self):
        # ["FCFS","SJF","SRTN","Prioridad no expropiativo","Prioridad expropiativo","Round Robin","Round Robin con Prioridad"]
        if self.indAlg==0:
            # FCFS
            if self.finPrograma:
                self.seleccionarPrioridad()
        elif self.indAlg in [1,2]:
            # SJF (No expropiativo), SJF (Expropiativo) = SRTN
            if self.finPrograma:
                self.seleccionarPrioridad()
        elif self.indAlg in [3,4]:
            # Prioridad no expropiativo, Prioridad expropiativo
            if self.finPrograma:
                self.seleccionarPrioridad()
        elif self.indAlg==5:
            # Round Robin
            pass
        else:
            # Round Robin con prioridad
            pass

    def seleccionarPrioridad(self):
        mayorPrioridad=None
        self.programaActual=None
        for i, programa in enumerate(self.listaProgramas):
            if mayorPrioridad==None or programa.prioridad>mayorPrioridad:
                if not programa.terminado:
                    mayorPrioridad=programa.prioridad
                    self.programaActual=i
            elif mayorPrioridad==programa.prioridad:
                datosProgAct=self.listaProgramas[self.programaActual]
                if datosProgAct.llegada>programa.llegada:
                    # Compara el tiempo de llegada si ambos programas tienen la misma prioridad
                    if not programa.terminado:
                        mayorPrioridad=programa.prioridad
                        self.programaActual=i
        try:
            self.apuntador=self.listaProgramas[self.programaActual].limites[0]
            self.finPrograma=False
            self.seccionInstrucciones.resetSeccion()
        except:
            self.abrirError("Ya no hay más programas por ejecutar")


    def iniciarCH(self):
        Window.clearcolor=(26/255, 28/255, 82/255, 0.8)
        Window.size=(1200,900)
        Window.top=540-Window.height/2
        Window.left=960-Window.width/2
        self.clear_widgets()
        if self.indAlg in [5,6]:
            self.abrirLecQuantum()
        self.rows=4
        self.padding=[10,10]
        #Atributos para el control de programas
        self.apuntador=None         #Indica la posición de memoria dónde se encuentra la siguiente instrucción a ser ejecutada
        self.programaValido=None    #Indica si el programa ha tenido algún error durante su ejecución
        self.finPrograma=None       #Indica si ya se han ejecutado todas las instrucciones del programa

        self.appExplorador=None
        self.valorLeido=None
        self.variableLeida=True
        self.listaProgramas=[]
        self.programaActual=0
        self.omitirLineasGlobal=[]
        self.vectorMemoria, self.posDispMem = func.inicializarMemoria(self.sizeKernel, self.sizeMemoria)
        
        # Acá se define la sección del título
        self.tituloPpal=Label(text="[b]CH-MÁQUINA[/b]", markup=True, size_hint_y=0.07, height=100, font_size="40sp")
        
        # Acá se definen la sección para cargar programas
        caja=BoxLayout(orientation="horizontal", height=50, size_hint_y=0.08, padding=[10,8,10,20], spacing=10)
        mensajeRuta=Label(text="Ruta del archivo: ", width=100, size_hint_x=0.2)
        self.textoRuta=TextInput(text="", readonly=True, width=200, size_hint_x=0.6)
        botonExplorador=Button(text="Buscar archivo", width=100, size_hint_x=0.2)
        botonExplorador.bind(on_release=self.abrirExplorador)
        #mensaje=Label(text="...")
        caja.add_widget(mensajeRuta)
        caja.add_widget(self.textoRuta)
        caja.add_widget(botonExplorador)

        # Acá se define la zona de muestra
        zonaMuestra=GridLayout(cols=3, size_hint_y=0.7,spacing=10)
        bloque=GridLayout(rows=2, spacing=10, size_hint_x=0.5)
        subzona1=GridLayout(cols=2, spacing=10, size_hint_x=0.6)
        subzona2=BoxLayout(orientation="horizontal", spacing=10, size_hint_y=0.4)

        self.seccionInstrucciones=SeccionInstrucciones(self)
        primeraColumna=self.seccionInstrucciones

        segundaColumna=BoxLayout(orientation="vertical", spacing=10)
        self.seccionVariables=SeccionVariables(self)
        self.seccionEtiquetas=SeccionEtiquetas(self)
        segundaColumna.add_widget(self.seccionVariables)
        segundaColumna.add_widget(self.seccionEtiquetas)

        self.seccionResultados=SeccionResultados(self, size_hint_x=0.25)
        terceraColumna=self.seccionResultados

        self.seccionMemoria=SeccionMemoria(self, size_hint_x=0.25)
        cuartaColumna=self.seccionMemoria

        self.seccionProgramas=SeccionProgramasMem(self)

        subzona1.add_widget(primeraColumna)
        subzona1.add_widget(segundaColumna)
        subzona2.add_widget(self.seccionProgramas)
        bloque.add_widget(subzona1)
        bloque.add_widget(subzona2)
        zonaMuestra.add_widget(bloque)
        zonaMuestra.add_widget(terceraColumna)
        zonaMuestra.add_widget(cuartaColumna)

        # Acá se definen los botones inferiores
        footer=BoxLayout(orientation="horizontal", size_hint_y=0.07, padding=[20,10], spacing=50)
        self.botonCargarArchivo=Button(text="Cargar archivo", border=[20,20,20,20])
        self.botonCargarArchivo.bind(on_release=self.cargarArchivo)
        self.botonEjecutarPaso=Button(text="Ejecutar paso", border=[20,20,20,20])
        self.botonEjecutarPaso.bind(on_release=self.ejecutarPaso)
        self.botonEjecutarPrograma=Button(text="Ejecutar programa", border=[20,20,20,20])
        self.botonEjecutarPrograma.bind(on_release=self.ejecutarPrograma)
        self.botonPantallaInicial=Button(text="Volver a la\nventana inicial", border=[20,20,20,20])
        self.botonPantallaInicial.bind(on_release=self.ventanaInicial)

        footer.add_widget(self.botonCargarArchivo)
        footer.add_widget(self.botonEjecutarPaso)
        footer.add_widget(self.botonEjecutarPrograma)
        footer.add_widget(self.botonPantallaInicial)

        # Acá se ensambla la vista principal
        self.add_widget(self.tituloPpal)
        self.add_widget(caja)
        self.add_widget(zonaMuestra)
        self.add_widget(footer)


    def abrirExplorador(self, obj):
        self.appExplorador=ExploradorApp(self, self.cerrar_Explorador)
        contenido=self.appExplorador.build()
        self._popup = Popup(title="Cargar archivo", content=contenido,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def cerrar_Explorador(self, obj):
        try:
            self.ruta=self.appExplorador.rutaCompleta
            self.textoRuta.text=self.ruta
        except:
            self.ruta=None
            self.textoRuta.text=""
        self._popup.dismiss()

    def abrirLecPrioridad(self):
        self.appLectura=LecturaValorApp(self, self.cerrarLecPrioridad, "IP100")
        contenido=self.appLectura.build()
        self._popup = Popup(title="Asignar prioridad", content=contenido,
                            size_hint=(0.4, 0.4))
        self._popup.open()

    def cerrarLecPrioridad(self, obj):
        try:
            self.valorLeido=self.appLectura.ventana.valorLeido
        except:
            self.valorLeido=None
        else:
            self.listaProgramas[self.programaLeido].cambiarPrioridad(self.valorLeido)
            self.seccionProgramas.resetSeccion()
        self._popup.dismiss()

    def abrirLecQuantum(self):
        self.appLectura=LecturaValorApp(self, self.cerrarLecQuantum, "IP100")
        contenido=self.appLectura.build()
        self._popup = Popup(title="Definir Quantum", content=contenido,
                            size_hint=(0.4, 0.4))
        self._popup.open()

    def cerrarLecQuantum(self, obj):
        try:
            self.valorLeido=self.appLectura.ventana.valorLeido
        except:
            self.valorLeido=None
        else:
            self.quantum=self.valorLeido
            self.tituloPpal.text+=f"Quantum: {self.quantum}"
        self._popup.dismiss()

    def abrirLectura(self):
        self.appLectura=LecturaValorApp(self, self.cerrarLectura, self.tipoVarLeida)
        contenido=self.appLectura.build()
        self._popup = Popup(title="Leer dato", content=contenido,
                            size_hint=(0.4, 0.4))
        self._popup.open()

    def cerrarLectura(self, obj):
        try:
            self.valorLeido=self.appLectura.ventana.valorLeido
            self.variableLeida=True
        except:
            self.valorLeido=None
        else:
            self.objetoVarLeida.setValor(self.valorLeido)
            self.vectorMemoria[self.posVarLeida]=self.objetoVarLeida
            self.seccionResultados.textoPantalla.text=str(self.valorLeido)
            self._popup.dismiss()

    def abrirError(self, mensaje, propSize=(0.4, 0.4)):
        self.appError=MensajeErrorApp(self, self.cerrar_Error, mensaje)
        contenido=self.appError.build()
        self._popup = Popup(title="Error", content=contenido,
                            size_hint=propSize)
        self._popup.open()

    def cerrar_Error(self, obj):
        self._popup.dismiss()

    def cargarArchivo(self, obj):
        try:
            x=self.ruta
        except:
            self.abrirError("No se ha seleccionado ningún archivo")
        else:
            try:
                if self.ruta[-3:]!=".ch":
                    self.abrirError("El formato del archivo es inválido")
                    return None
                tupla=func.cargarPrograma(self.ruta, self.posDispMem, self.vectorMemoria, self.omitirLineasGlobal, self.listaProgramas)
                if tupla[0]==False:
                    self.abrirError(tupla[1])
                    return None
                else:
                    __, self.vectorMemoria, self.posDispMem, self.omitirLineasGlobal, self.listaProgramas=tupla

                print(self.listaProgramas)

                try:
                    if self.listaProgramas[-1]==self.listaProgramas[self.programaActual]: 
                        self.apuntador=self.listaProgramas[self.programaActual].limites[0]
                except IndexError:
                    self.abrirError("El archivo no es válido")
                else:
                    self.programaValido=None
                    self.finPrograma=None
                    self.programaLeido=len(self.listaProgramas)-1
                    self.cargarAlgoritmo()
                    self.seccionInstrucciones.resetSeccion()

                    self.seccionVariables.resetSeccion()

                    self.seccionEtiquetas.resetSeccion()

                    self.seccionResultados.textoPantalla.text=". . ."
                    self.seccionResultados.textoImpreso.text=". . ."

                    self.seccionProgramas.resetSeccion()

                    self.seccionMemoria.scroll.actualizarDatosMem()
            except TypeError as e:
                print(e)
                self.abrirError("El archivo no es válido.")

    def ejecutarPaso(self, obj):
        if len(self.listaProgramas)==0:
            self.abrirError("No hay programas cargados en memoria")
            return None
        elif self.programaValido==False or self.finPrograma==True:
            self.abrirError("No se puede hacer más")
            return None
        elif self.variableLeida==False:
            self.abrirError("Aún no se ha leído la variable")
            self.apuntador=self.apPrev
            return None

        self.apPrev=self.apuntador
        valido=True                             #Se asume que el funcionamiento es correcto
        fin=False                               #Se asume que la línea no es de retorno
        try:
            programaActual=self.programaActual
        except AttributeError:
            self.abrirError("No se ha seleccionado ningún programa")
        else:
            posVariablesMem=self.listaProgramas[programaActual].posVariablesMem
            diccEtiquetas=self.listaProgramas[programaActual].diccEtiquetas
            linea=self.vectorMemoria[self.apuntador]
            tipoDato=type(self.vectorMemoria[self.apuntador])
            aritmeticos=["sume", "reste", "multiplique", "divida", "potencia", "modulo"]
            proxDirecc=self.apuntador+1
            if self.apuntador not in self.omitirLineasGlobal and tipoDato!=func.Variable and linea!=None:
                linea=linea.split()
                comando=linea[0]
                if comando=="nueva" or comando=="etiqueta":
                    pass
                elif comando=="cargue":
                    #Se traen los datos de la variable a cargar al acumulador
                    variable=linea[1]
                    posVar=posVariablesMem[variable]
                    objetoVar=self.vectorMemoria[posVar]
                    valor=objetoVar.getValor()
                    tipo=objetoVar.getTipo()

                    #Se suben los datos al acumulador
                    objetoAcum=self.vectorMemoria[0]
                    objetoAcum.setTipo(tipo)
                    objetoAcum.setValor(valor)
                    self.vectorMemoria[0]=objetoAcum
                elif comando=="almacene":
                    #Se cargan los datos de la variable a sobreescribir
                    variable=linea[1]
                    posVar=posVariablesMem[variable]
                    objetoVar=self.vectorMemoria[posVar]
                    tipoVar=objetoVar.getTipo()

                    #Se obtiene el tipo de dato del acumulador
                    objetoAcum=self.vectorMemoria[0]
                    tipoAcum=objetoAcum.getTipo()

                    if tipoVar==tipoAcum:               #Se comprueba que el tipo de dato del acumulador es el mismo que el tipo de dato de la variable
                        valorAcum=objetoAcum.getValor()
                        objetoVar.setValor(valorAcum)
                        self.vectorMemoria[posVar]=objetoVar
                    elif tipoVar=="I" and tipoAcum=="R":
                        valorAcum=objetoAcum.getValor()
                        objetoVar.setValor(int(valorAcum))
                        self.vectorMemoria[posVar]=objetoVar
                    else:
                        self.abrirError(f"Tipo de dato inválido {tipoVar} y {tipoAcum} no son equivalentes.")
                        valido=False          
                elif comando in aritmeticos:
                    variable=linea[1]                       #Recupera el nombre de la variable pasada como parámetro
                    posVar=posVariablesMem[variable]        #Halla la posición en memoria de dicha variable
                    objetoVar=self.vectorMemoria[posVar]    #Se recupera lo que hay en dicha posición de memoria
                    tipoVar=objetoVar.getTipo()             #Se pide el tipo de dato que alberga la variable
                    if tipoVar!="I" and tipoVar!="R":
                        self.abrirError(f"La variable {variable} no tiene el tipo de dato entero o real, por lo tanto no se puede realizar la operación.")
                        valido=False
                    else:
                        valorVar=objetoVar.getValor()       #Se pide el valor de la variable recuperada
                        objetoAcum=self.vectorMemoria[0]    #Se accede al acumulador
                        tipoAcum=objetoAcum.getTipo()       #Se pide el tipo de dato que alberga el acumulador
                        if tipoAcum!="I" and tipoAcum!="R":
                            self.abrirError(f"El acumulador no tiene el tipo de dato entero o real, por lo tanto no se puede realizar la operación.")
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
                                    self.abrirError(f"El valor del divisor es 0. El programa no puede continuar.")
                                    valido=False
                                elif comando=="divida":
                                    valorAcum/=valorVar
                                elif comando=="modulo":
                                    valorAcum%=valorVar
                                elif comando=="potencia" and tipoVar=="I": 
                                    valorAcum=pow(valorAcum, valorVar)
                                else:
                                    self.abrirError(f"El valor del exponente no es entero ({valorVar}). El programa no puede continuar.")
                                    valido=False

                            if valido:
                                objetoAcum.setValor(valorAcum)
                                self.vectorMemoria[0]=objetoAcum
                elif comando=="vaya":
                    etiqueta=linea[1]
                    proxDirecc=diccEtiquetas[etiqueta]
                elif comando=="vayasi":
                    objetoAcum=self.vectorMemoria[0]
                    tipoAcum=objetoAcum.getTipo()
                    if tipoAcum=="C":
                        return False
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
                        objeto=self.vectorMemoria[posVar]
                    else:
                        objeto=self.vectorMemoria[0]
                    valor=objeto.getValor()
                    self.seccionResultados.textoPantalla.text=str(valor)
                elif comando=="imprima":
                    variable=linea[1]
                    if variable!="acumulador":
                        posVar=posVariablesMem[variable]
                        objeto=self.vectorMemoria[posVar]
                    else:
                        objeto=self.vectorMemoria[0]
                    valor=objeto.getValor()
                    self.seccionResultados.textoImpreso.text=str(valor)
                elif comando=="retorne":
                    fin=True
                    self.listaProgramas[self.programaActual].terminarPrograma()
                elif comando=="concatene":
                    variable=linea[1]
                    posVar=posVariablesMem[variable]
                    objetoVar=self.vectorMemoria[posVar]
                    tipoVar=objetoVar.getTipo()
                    if tipoVar!="C":
                        self.abrirError("El valor de la variable a concatenar no es una cadena")
                        valido=False
                    else:
                        valorVar=objetoVar.getValor()   
                        objetoAcum=self.vectorMemoria[0]
                        valorAcum=objetoAcum.getValor()+valorVar
                        objetoAcum.setValor(valorAcum)
                        objetoAcum.setTipo(tipoVar)
                        self.vectorMemoria[0]=objetoAcum
                elif comando=="elimine":
                    variable=linea[1]
                    posVar=posVariablesMem[variable]
                    objetoVar=self.vectorMemoria[posVar]
                    tipoVar=objetoVar.getTipo()
                    if tipoVar!="C":
                        self.abrirError(f"El valor de la variable a eliminar no es una cadena. Su tipo es {tipoVar}")
                        valido=False
                    else:
                        objetoAcum=self.vectorMemoria[0]
                        tipoAcum=objetoAcum.getTipo()
                        if tipoAcum!="C":
                            self.abrirError(f"El valor en el acumulador es de tipo {tipoAcum} y no es una cadena, no se puede continuar con la operación.")
                            valido=False
                        else:
                            valorVar=objetoVar.getValor() 
                            valorAcum=objetoAcum.getValor()
                            valorAcum=func.eliminarSubcadena(valorAcum,valorVar)
                            objetoAcum.setValor(valorAcum)
                            self.vectorMemoria[0]=objetoAcum
                elif comando=="extraiga":
                    variable=linea[1]
                    posVar=posVariablesMem[variable]
                    objetoVar=self.vectorMemoria[posVar]
                    tipoVar=objetoVar.getTipo()
                    if tipoVar!="I":
                        self.abrirError(f"El tipo de la variable no es válido para la operación. Tipo de la variable: {tipoVar}")
                        valido=False
                    else:
                        objetoAcum=self.vectorMemoria[0]
                        tipoAcum=objetoAcum.getTipo()
                        if tipoAcum!="C":
                            self.abrirError(f"El tipo de variable en el acumulador no es una cadena, no se puede continuar con la operación. Su tipo es: {tipoAcum}")
                            valido=False
                        else:
                            valorVar=objetoVar.getValor()
                            valorAcum=objetoAcum.getValor()
                            if valorVar>len(valorAcum):
                                valorVar=len(valorAcum)
                            valorAcum=valorAcum[:valorVar]
                            objetoAcum.setValor(valorAcum)
                            self.vectorMemoria[0]=objetoAcum
                elif comando=="Y" or comando=="O":
                    variable1=linea[1]
                    posVar1=posVariablesMem[variable1]
                    objetoVar1=self.vectorMemoria[posVar1]
                    tipoVar1=objetoVar1.getTipo()
                    if tipoVar1!="L":
                        self.abrirError(f"Tipo de dato inválido: {tipoVar1}")
                        valido=False
                    else:
                        variable2=linea[2]
                        posVar2=posVariablesMem[variable2]
                        objetoVar2=self.vectorMemoria[posVar2]
                        tipoVar2=objetoVar2.getTipo()
                        if tipoVar2!="L":
                            self.abrirError(f"Tipo de dato inválido: {tipoVar2}")
                            valido=False
                        else:
                            variable3=linea[3]
                            posVar3=posVariablesMem[variable3]
                            objetoVar3=self.vectorMemoria[posVar3]
                            tipoVar3=objetoVar3.getTipo()
                            if tipoVar3!="L":
                                self.abrirError(f"Tipo de dato inválido: {tipoVar3}")
                                valido=False
                            else:
                                valorVar1=objetoVar1.getValor()
                                valorVar2=objetoVar2.getValor()
                                if comando=="Y":
                                    valorVar3=valorVar1 & valorVar2
                                else: # comando=="O"
                                    valorVar3=valorVar1 | valorVar2
                                objetoVar3.setValor(valorVar3)
                                self.vectorMemoria[posVar3]=objetoVar3
                elif comando=="NO":
                    variable1=linea[1]
                    posVar1=posVariablesMem[variable1]
                    objetoVar1=self.vectorMemoria[posVar1]
                    tipoVar1=objetoVar1.getTipo()
                    if tipoVar1!="L":
                        self.abrirError(f"Tipo de dato inválido: {tipoVar1}")
                        valido=False
                    else:
                        variable2=linea[2]
                        posVar2=posVariablesMem[variable2]
                        objetoVar2=self.vectorMemoria[posVar2]
                        tipoVar2=objetoVar2.getTipo()
                        if tipoVar2!="L":
                            self.abrirError(f"Tipo de dato inválido: {tipoVar2}")
                            valido=False
                        else:
                            valorVar1=objetoVar1.getValor()
                            if not valorVar1 == False:
                                valorVar2=0
                            else:
                                valorVar2=1
                            objetoVar2.setValor(valorVar2)
                            self.vectorMemoria[posVar2]=objetoVar2
                elif comando=="lea":
                    variable1=linea[1]
                    self.posVarLeida=posVariablesMem[variable1]
                    self.objetoVarLeida=self.vectorMemoria[self.posVarLeida]
                    self.tipoVarLeida=self.objetoVarLeida.getTipo()
                    self.variableLeida=False
                    self.abrirLectura()
                elif comando=="logaritmo":
                    variable1=linea[1]
                    posVar1=posVariablesMem[variable1]
                    objetoVar1=self.vectorMemoria[posVar1]
                    tipoVar1=objetoVar1.getTipo()
                    if tipoVar=="C" or tipoVar=="L":
                        self.abrirError(f"Tipo de dato inválido en la variable: {tipoVar1}")
                        valido=False
                    else:
                        base=objetoVar1.getValor()
                        if base<=1:
                            self.abrirError(f"La base del logaritmo es inválida: {base}")
                            valido=False
                        else:
                            objetoAcum=self.vectorMemoria[0]    #Se accede al acumulador
                            tipoAcum=objetoAcum.getTipo() 
                            if tipoAcum=="C" or tipoAcum=="L":
                                self.abrirError(f"Tipo de dato inválido en el acumulador: {tipoAcum}")
                                valido=False
                            else:
                                potencia=objetoAcum.getValor()
                                if potencia<1:
                                    self.abrirError(f"La potencia del logaritmo es inválida: {potencia}")
                                    valido=False
                                else:
                                    logaritmo=log(potencia, base)
                                    objetoAcum.setValor(logaritmo)
                                    self.vectorMemoria[0]=objetoAcum
            else:   #Se detectan los comentarios o líneas en blanco
                pass

            if not valido:
                self.programaValido=False
                return None

            self.listaProgramas[programaActual].cambiarIns(proxDirecc)
            self.apuntador=proxDirecc
            self.programaValido=valido
            self.finPrograma=fin
            self.pasoAlgoritmo()
            self.seccionInstrucciones.scroll.actualizarIns()
            self.seccionMemoria.scroll.actualizarDatosMem()
            self.seccionProgramas.resetSeccion()

    def ejecutarPrograma(self, obj):
        if len(self.listaProgramas)==0:
            self.abrirError("No hay programas cargados en memoria")
            return None
        elif self.variableLeida==False:
            self.abrirError("Aún no se ha leído la variable")
            return None
        while True:
            self.ejecutarPaso(obj)
            if self.programaValido==False or self.finPrograma==True or self.variableLeida==False:
                break


class CHMaquinaApp(App):

    def build(self):
        return VentanaPrincipal(self)


if __name__ == '__main__':
    CHMaquinaApp().run()