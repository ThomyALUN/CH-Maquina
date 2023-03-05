from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from math import log

from explorador import *
from secciones import *
from lecturaValor import *

class VentanaPrincipal(GridLayout):

    def __init__(self, **kwargs):
        super(VentanaPrincipal, self).__init__(**kwargs)
        self.size=(1000,1000)
        self.rows=4
        self.padding=[10,10]
        #Atributos para el control de programas
        self.apuntador=None         #Indica la posición de memoria dónde se encuentra la siguiente instrucción a ser ejecutada
        self.programaValido=None    #Indica si el programa ha tenido algún error durante su ejecución
        self.finPrograma=None       #Indica si ya se han ejecutado todas las instrucciones del programa

        self.finDocumento=1
        self.appExplorador=None
        self.valorLeido=None
        self.variableLeida=True
        self.listaProgramas=[]
        self.omitirLineasGlobal=[]
        self.vectorMemoria, self.posDispMem = func.inicializarMemoria(self.finDocumento)
        
        # Acá se define la sección del título
        self.tituloPpal=Label(text="[b]CH-MÁQUINA[/b]", markup=True, size_hint_y=0.08, height=100, font_size="40sp")
        
        # Acá se definen la sección para cargar programas
        caja=BoxLayout(orientation="horizontal", height=50, size_hint_y=0.12, padding=[10,8,10,20], spacing=10)
        mensajeRuta=Label(text="Ruta del archivo: ", width=100, size_hint_x=0.2)
        self.textoRuta=TextInput(text="", readonly=True, width=200, size_hint_x=0.6)
        botonExplorador=Button(text="Buscar archivo", width=100, size_hint_x=0.2)
        botonExplorador.bind(on_release=self.abrirExplorador)
        #mensaje=Label(text="...")
        caja.add_widget(mensajeRuta)
        caja.add_widget(self.textoRuta)
        caja.add_widget(botonExplorador)

        # Acá se define la zona de muestra
        zonaMuestra=GridLayout(cols=5, size_hint_y=0.6)

        self.seccionInstrucciones=SeccionInstrucciones(self)
        primeraColumna=self.seccionInstrucciones

        segundaColumna=BoxLayout(orientation="vertical")
        self.seccionVariables=SeccionVariables(self)
        self.seccionEtiquetas=SeccionEtiquetas(self)
        segundaColumna.add_widget(self.seccionVariables)
        segundaColumna.add_widget(self.seccionEtiquetas)

        self.seccionResultados=SeccionResultados(self)
        terceraColumna=self.seccionResultados

        self.seccionMemoria=SeccionMemoria(self)
        cuartaColumna=self.seccionMemoria

        zonaMuestra.add_widget(primeraColumna)
        zonaMuestra.add_widget(segundaColumna)
        zonaMuestra.add_widget(terceraColumna)
        zonaMuestra.add_widget(cuartaColumna)

        # Acá se definen los botones inferiores
        footer=BoxLayout(orientation="horizontal", size_hint_y=0.08, padding=[20,10], spacing=50)
        self.botonCargarArchivo=Button(text="Cargar archivo", width=100, border=[20,20,20,20])
        self.botonCargarArchivo.bind(on_release=self.cargarArchivo)
        self.botonEjecutarPaso=Button(text="Ejecutar paso", width=100, border=[20,20,20,20])
        self.botonEjecutarPaso.bind(on_release=self.ejecutarPaso)
        self.botonEjecutarPrograma=Button(text="Ejecutar programa", width=100, border=[20,20,20,20])
        self.botonEjecutarPrograma.bind(on_release=self.ejecutarPrograma)

        footer.add_widget(self.botonCargarArchivo)
        footer.add_widget(self.botonEjecutarPaso)
        footer.add_widget(self.botonEjecutarPrograma)

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

    def abrirLectura(self):
        self.appLectura=LecturaValorApp(self, self.cerrar_Lectura, self.tipoVarLeida)
        contenido=self.appLectura.build()
        self._popup = Popup(title="Leer dato", content=contenido,
                            size_hint=(0.4, 0.4))
        self._popup.open()

    def cerrar_Lectura(self, obj):
        try:
            self.valorLeido=self.appLectura.ventana.valorLeido
            self.variableLeida=True
        except:
            self.valorLeido=None
        else:
            self.objetoVarLeida.setValor(self.valorLeido)
            self.vectorMemoria[self.posVarLeida]=self.objetoVarLeida
        self._popup.dismiss()

    def cargarArchivo(self, obj):
        try:
            print(self.ruta)
        except:
            pass
        else:
            try:
                tupla=func.cargarPrograma(self.ruta, self.posDispMem, self.vectorMemoria, self.omitirLineasGlobal, self.listaProgramas)
                if tupla==False:
                    pass
                else:
                    __, self.vectorMemoria, self.posDispMem, self.omitirLineasGlobal, self.listaProgramas=tupla

                self.programaActual=len(self.listaProgramas)-1
                print(self.listaProgramas)

                try:
                    self.apuntador=self.listaProgramas[self.programaActual][0][0]
                except IndexError:
                    print("El archivo no es válido")
                else:
                    self.programaValido=None
                    self.finPrograma=None
                    self.seccionInstrucciones.resetSeccion()

                    self.seccionVariables.clear_widgets()
                    self.seccionVariables.__init__(self)

                    self.seccionEtiquetas.clear_widgets()
                    self.seccionEtiquetas.__init__(self)

                    self.seccionResultados.textoPantalla.text=""
                    self.seccionResultados.textoImpreso.text=""

                    self.seccionMemoria.clear_widgets()
                    self.seccionMemoria.__init__(self)
            except TypeError:
                print("No se seleccionó ningún archivo")

    def ejecutarPaso(self, obj):
        #Función incompleta
        if len(self.listaProgramas)==0:
            print("Error")
            return None
        elif self.programaValido==False or self.finPrograma==True:
            print("No se puede hacer más")
            return None
        elif self.variableLeida==False:
            print("Aún no se ha leído la variable")
            return None

        valido=True                             #Se asume que el funcionamiento es correcto
        fin=False                               #Se asume que la línea no es de retorno
        try:
            programaActual=self.programaActual
        except AttributeError:
            print("Error")
        else:
            posVariablesMem=self.listaProgramas[programaActual][1]
            diccEtiquetas=self.listaProgramas[programaActual][2]
            linea=self.vectorMemoria[self.apuntador]
            tipoDato=type(self.vectorMemoria[self.apuntador])
            aritmeticos=["sume", "reste", "multiplique", "divida", "potencia", "modulo"]
            proxDirecc=self.apuntador+1
            if self.apuntador not in self.omitirLineasGlobal and tipoDato!=func.Variable and linea!=None:
                linea=linea.split()
                comando=linea[0]
                print(f"{self.apuntador}:{linea}",end="")
                if comando=="nueva" or comando=="etiqueta":
                    print(f" :Línea ignorada", end="")
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
                    
                    #print(f": Variable a cargar {variable}:{posVar}:{vectorMemoria[posVar]}:Valor={valor}:Tipo={tipo}")
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
                        print(f"\nTipo de dato inválido {tipoVar} y {tipoAcum} no son equivalentes.")
                        valido=False          
                elif comando in aritmeticos:
                    variable=linea[1]                       #Recupera el nombre de la variable pasada como parámetro
                    posVar=posVariablesMem[variable]        #Halla la posición en memoria de dicha variable
                    objetoVar=self.vectorMemoria[posVar]    #Se recupera lo que hay en dicha posición de memoria
                    tipoVar=objetoVar.getTipo()             #Se pide el tipo de dato que alberga la variable
                    if tipoVar!="I" and tipoVar!="R":
                        print(f"La variable {variable} no tiene el tipo de dato entero o real, por lo tanto no se puede realizar la operación.")
                        valido=False
                    else:
                        valorVar=objetoVar.getValor()       #Se pide el valor de la variable recuperada
                        objetoAcum=self.vectorMemoria[0]    #Se accede al acumulador
                        tipoAcum=objetoAcum.getTipo()       #Se pide el tipo de dato que alberga el acumulador
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
                elif comando=="concatene":
                    variable=linea[1]
                    posVar=posVariablesMem[variable]
                    objetoVar=self.vectorMemoria[posVar]
                    tipoVar=objetoVar.getTipo()
                    if tipoVar!="C":
                        print("El valor de la variable a concatenar no es una cadena")
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
                        print("El valor de la variable a eliminar no es una cadena")
                        valido=False
                    else:
                        objetoAcum=self.vectorMemoria[0]
                        tipoAcum=objetoAcum.getTipo()
                        if tipoAcum!="C":
                            print("El valor en el acumulador no es una cadena, no se puede continuar con la operación")
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
                        print("El valor de la variable no es válido para la operación")
                        valido=False
                    else:
                        objetoAcum=self.vectorMemoria[0]
                        tipoAcum=objetoAcum.getTipo()
                        if tipoAcum!="C":
                            print("El valor en el acumulador no es una cadena, no se puede continuar con la operación")
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
                        print("Tipo de dato inválido")
                        valido=False
                    else:
                        variable2=linea[2]
                        posVar2=posVariablesMem[variable2]
                        objetoVar2=self.vectorMemoria[posVar2]
                        tipoVar2=objetoVar2.getTipo()
                        if tipoVar2!="L":
                            print("Tipo de dato inválido")
                            valido=False
                        else:
                            variable3=linea[3]
                            posVar3=posVariablesMem[variable3]
                            objetoVar3=self.vectorMemoria[posVar3]
                            tipoVar3=objetoVar3.getTipo()
                            if tipoVar3!="L":
                                print("Tipo de dato inválido")
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
                        print("Tipo de dato inválido")
                        valido=False
                    else:
                        variable2=linea[2]
                        posVar2=posVariablesMem[variable2]
                        objetoVar2=self.vectorMemoria[posVar2]
                        tipoVar2=objetoVar2.getTipo()
                        if tipoVar2!="L":
                            print("Tipo de dato inválido")
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
                        print("Tipo de dato inválido en la variable")
                        valido=False
                    else:
                        base=objetoVar1.getValor()
                        if base<=1:
                            print("La base del loagritmo es inválida")
                            valido=False
                        else:
                            objetoAcum=self.vectorMemoria[0]    #Se accede al acumulador
                            tipoAcum=objetoAcum.getTipo() 
                            if tipoAcum=="C" or tipoAcum=="L":
                                print("Tipo de dato inválido en el acumulador")
                                valido=False
                            else:
                                potencia=objetoAcum.getValor()
                                if potencia<1:
                                    print("La potencia del loagritmo es inválida")
                                    valido=False
                                else:
                                    logaritmo=log(potencia, base)
                                    objetoAcum.setValor(logaritmo)
                                    self.vectorMemoria[0]=objetoAcum
            else:   #Se detectan los comentarios o líneas en blanco
                print(f"{self.apuntador}: Linea omitida",end="")

            print("")

            self.apuntador=proxDirecc
            self.programaValido=valido
            self.finPrograma=fin
            self.seccionInstrucciones.scroll.actualizarIns()
            self.seccionMemoria.scroll.actualizarDatosMem()

    def ejecutarPrograma(self, obj):
        if len(self.listaProgramas)==0 or self.variableLeida==False:
            print("Error")
            return None
        while True:
            self.ejecutarPaso(obj)
            if self.programaValido==False or self.finPrograma==True or self.variableLeida==False:
                break




class CHMaquinaApp(App):

    def build(self):
        Window.clearcolor=(26/255, 28/255, 82/255, 0.8)
        Window.size=(900,650)
        return VentanaPrincipal()

if __name__ == '__main__':
    CHMaquinaApp().run()