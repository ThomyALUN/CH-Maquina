from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window

from explorador import *
import funciones as func


class SeccionInstrucciones(GridLayout):

    def __init__(self, app, **kwargs):
        super(SeccionInstrucciones, self).__init__(**kwargs)
        self.rows=2
        self.app=app
        self.titulo=GridLayout(cols=2, height=60, size_hint_y=None)

        etiqueta1=Label(text="[b]Posición[/b]",size_hint_y=None, markup=True)
        etiqueta2=Label(text="[b]Instrucción[/b]",size_hint_y=None, markup=True)
        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)

        if app.listaProgramas==[]:
            self.scroll=BoxLayout(orientation="horizontal")
            self.scroll.add_widget(Label(text="- - -"))
            self.scroll.add_widget(Label(text="- - -"))
        else:
            self.scroll=ScrollInstrucciones(self.app)

        self.add_widget(self.titulo)
        self.add_widget(self.scroll)


class ScrollInstrucciones(ScrollView):
    def __init__(self, app, **kwargs):
        super(ScrollInstrucciones, self).__init__(**kwargs)
        self.app=app
        vectorMemoria=app.vectorMemoria
        programaActual=app.programaActual
        columnaInstrucciones=GridLayout(cols=2, spacing=5, size_hint_y=None)
        # Permite que se mueva a través de todos los datos
        columnaInstrucciones.bind(minimum_height=columnaInstrucciones.setter('height'))

        limites=app.listaProgramas[programaActual][0]
        
        for pos in range(limites[0],limites[1]):
            instruccion=vectorMemoria[pos]
            mensaje1=f"{func.agregarCeros(pos,4)}"
            mensaje2=f"{instruccion}"
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, height=40, width=100)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, height=40, width=100)
            columnaInstrucciones.add_widget(etiqueta1)
            columnaInstrucciones.add_widget(etiqueta2)
        self.add_widget(columnaInstrucciones)


class SeccionVariables(GridLayout):

    def __init__(self, app, **kwargs):
        super(SeccionVariables, self).__init__(**kwargs)
        self.rows=2
        self.app=app

        self.titulo=GridLayout(cols=2, height=60, size_hint_y=None)

        etiqueta1=Label(text="[b]Posición[/b]",size_hint_y=None, markup=True)
        etiqueta2=Label(text="[b]Variable[/b]",size_hint_y=None, markup=True)
        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)

        if app.listaProgramas==[]:
            self.scroll=BoxLayout(orientation="horizontal")
            self.scroll.add_widget(Label(text="- - -"))
            self.scroll.add_widget(Label(text="- - -"))
        else:
            self.scroll=ScrollVariables(self.app)

        self.add_widget(self.titulo)
        self.add_widget(self.scroll)

    def reset(self):
        self.scroll=ScrollVariables(self.app)


class ScrollVariables(ScrollView):

    def __init__(self, app, **kwargs):
        super(ScrollVariables, self).__init__(**kwargs)
        self.app=app

        columnaVariables=GridLayout(cols=2, spacing=5, size_hint_y=None)
        # Permite que se mueva a través de todos los datos
        columnaVariables.bind(minimum_height=columnaVariables.setter('height'))

        listaVar=[]
        for programa in range(len(self.app.listaProgramas)):
            posVariablesMem=self.app.listaProgramas[programa][1]
            for variable, pos in posVariablesMem.items():
                nombreVariable=func.agregarCeros(programa,4)+variable
                listaVar.append([pos,nombreVariable])
        listaVar.sort()
        
        for pos, variable in listaVar:
            mensaje1=f"{func.agregarCeros(pos,4)}"
            mensaje2=f"{variable}"
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, height=40, width=100)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, height=40, width=100)
            columnaVariables.add_widget(etiqueta1)
            columnaVariables.add_widget(etiqueta2)
        self.add_widget(columnaVariables)


class SeccionEtiquetas(GridLayout):

    def __init__(self, app, **kwargs):
        super(SeccionEtiquetas, self).__init__(**kwargs)
        self.rows=2
        self.app=app
        self.titulo=GridLayout(cols=2, height=60, size_hint_y=None)

        etiqueta1=Label(text="[b]Posición[/b]",size_hint_y=None, markup=True)
        etiqueta2=Label(text="[b]Etiqueta[/b]",size_hint_y=None, markup=True)

        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)

        if app.listaProgramas==[]:
            self.scroll=BoxLayout(orientation="horizontal")
            self.scroll.add_widget(Label(text="- - -"))
            self.scroll.add_widget(Label(text="- - -"))
        else:
            self.scroll=ScrollEtiquetas(self.app)

        self.add_widget(self.titulo)
        self.add_widget(self.scroll)

    def setScroll(self,diccEtiquetas):
        self.scroll=ScrollEtiquetas(diccEtiquetas)


class ScrollEtiquetas(ScrollView):

    def __init__(self, app, **kwargs):
        super(ScrollEtiquetas, self).__init__(**kwargs)
        self.app=app

        columnaEtiquetas=GridLayout(cols=2, spacing=5, size_hint_y=None)
        # Permite que se mueva a través de todos los datos
        columnaEtiquetas.bind(minimum_height=columnaEtiquetas.setter('height'))

        listaEtiquetas=[]
        for programa in range(len(self.app.listaProgramas)):
            diccEtiquetas=self.app.listaProgramas[programa][2]
            for etiqueta, pos in diccEtiquetas.items():
                nombreEtiqueta=func.agregarCeros(programa,4)+etiqueta
                listaEtiquetas.append([pos,nombreEtiqueta])
        listaEtiquetas.sort()
        
        for pos, Etiqueta in listaEtiquetas:
            mensaje1=f"{func.agregarCeros(pos,4)}"
            mensaje2=f"{Etiqueta}"
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, height=40, width=100)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, height=40, width=100)
            columnaEtiquetas.add_widget(etiqueta1)
            columnaEtiquetas.add_widget(etiqueta2)
        self.add_widget(columnaEtiquetas)


class SeccionResultados(GridLayout):

    def __init__(self, **kwargs):
        super(SeccionResultados, self).__init__(**kwargs)
        self.rows=2
        resultados=GridLayout(rows=2)

        pantalla=GridLayout(rows=2, size_hint_y=0.5)
        etiqueta1=Label(text="[b]PANTALLA[/b]",size_hint_y=None, markup=True)
        cajaTexto=GridLayout(rows=1,padding=[10,10])
        espacioInteraccion=TextInput(text="...",readonly=True)
        cajaTexto.add_widget(espacioInteraccion)

        self.cajaTexto=cajaTexto
        pantalla.add_widget(etiqueta1)
        pantalla.add_widget(cajaTexto)

        impresora=GridLayout(rows=2, size_hint_y=0.5)
        etiqueta2=Label(text="[b]IMPRESORA[/b]",size_hint_y=None, markup=True)
        textoImpreso=Label(text="...")
        self.textoImpreso=textoImpreso
        impresora.add_widget(etiqueta2)
        impresora.add_widget(textoImpreso)

        resultados.add_widget(pantalla)
        resultados.add_widget(impresora)

        self.add_widget(resultados)

    def setScroll(self,instrucciones):
        #self.scroll=ScrollInstruucciones(instrucciones)
        pass


class SeccionMemoria(GridLayout):

    def __init__(self, app, **kwargs):
        super(SeccionMemoria, self).__init__(**kwargs)
        self.rows=2
        self.app=app
        self.titulo=GridLayout(cols=2, height=60, size_hint_y=0.2)

        etiqueta1=Label(text="[b]Posición[/b]",size_hint_y=None, markup=True)
        etiqueta2=Label(text="[b]Memoria[/b]",size_hint_y=None, markup=True)

        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)
        self.scroll=ScrollMemoria(self.app)

        self.add_widget(self.titulo)
        self.add_widget(self.scroll)
    
    def setScroll(self):
        self.scroll=ScrollMemoria(self.app)


class ScrollMemoria(ScrollView):

    def __init__(self, app, **kwargs):
        super(ScrollMemoria, self).__init__(**kwargs)
        columnaMemoria=GridLayout(cols=2, spacing=5, size_hint_y=None)
        # Permite que se mueva a través de todos los datos
        columnaMemoria.bind(minimum_height=columnaMemoria.setter('height'))
        

        for pos, direccionMem in enumerate(app.vectorMemoria):
            mensaje1=f"{func.agregarCeros(pos,4)}"
            if type(direccionMem)==func.Acumulador:
                mensaje2=f"{direccionMem.getValor()}"
            elif type(direccionMem)==func.Kernel:
                mensaje2="Kernel"
            elif type(direccionMem)==func.Variable:
                mensaje2=f"{direccionMem.getValor()}"
            elif direccionMem==None:
                mensaje2=""
            else:
                mensaje2=f"{direccionMem}"
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, height=40, width=100)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, height=40, width=100)
            columnaMemoria.add_widget(etiqueta1)
            columnaMemoria.add_widget(etiqueta2)
        self.add_widget(columnaMemoria)


class VentanaPrincipal(GridLayout):

    def __init__(self, **kwargs):
        super(VentanaPrincipal, self).__init__(**kwargs)
        self.size=(1000,1000)
        self.rows=4
        
        self.finDocumento=1
        self.appExplorador=None
        self.listaProgramas=[]
        self.omitirLineasGlobal=[]
        self.vectorMemoria, self.posDispMem = func.inicializarMemoria(self.finDocumento)
        
        # Acá se define la sección del título
        self.tituloPpal=Label(text="[b]CH-MÁQUINA[/b]", markup=True, size_hint_y=0.1, height=100, font_size="40sp")
        
        # Acá se definen la sección para cargar programas
        caja=BoxLayout(orientation="horizontal", height=50, size_hint_y=0.08, padding=[20,10], spacing=200)
        botonExplorador=Button(text="Buscar archivo", width=100, border=[20,20,20,20])
        botonExplorador.bind(on_release=self.abrirExplorador)
        mensaje=Button(text="Imprimir archivo", width=100, border=[20,20,20,20])
        mensaje.bind(on_release=self.mostrarArchivo)
        #mensaje=Label(text="...")
        caja.add_widget(botonExplorador)
        caja.add_widget(mensaje)

        # Acá se define la zona de muestra
        zonaMuestra=GridLayout(cols=5, size_hint_y=0.6)

        self.seccionInstrucciones=SeccionInstrucciones(self)
        primeraColumna=self.seccionInstrucciones

        segundaColumna=BoxLayout(orientation="vertical")
        self.seccionVariables=SeccionVariables(self)
        self.seccionEtiquetas=SeccionEtiquetas(self)
        segundaColumna.add_widget(self.seccionVariables)
        segundaColumna.add_widget(self.seccionEtiquetas)

        self.seccionResultados=SeccionResultados()
        terceraColumna=self.seccionResultados

        self.seccionMemoria=SeccionMemoria(self)
        cuartaColumna=self.seccionMemoria

        zonaMuestra.add_widget(primeraColumna)
        zonaMuestra.add_widget(segundaColumna)
        zonaMuestra.add_widget(terceraColumna)
        zonaMuestra.add_widget(cuartaColumna)

        # Acá se definen los botones inferiores
        footer=BoxLayout(orientation="horizontal", size_hint_y=0.08, padding=[20,10], spacing=50)
        botonCargarArchivo=Button(text="Cargar archivo", width=100, border=[20,20,20,20])
        botonCargarArchivo.bind(on_release=self.cargarArchivo)
        botonEjecutarPaso=Button(text="Ejecutar paso", width=100, border=[20,20,20,20])
        botonEjecutarPrograma=Button(text="Ejecutar programa", width=100, border=[20,20,20,20])

        footer.add_widget(botonCargarArchivo)
        footer.add_widget(botonEjecutarPaso)
        footer.add_widget(botonEjecutarPrograma)

        # Acá se ensambla la vista principal
        self.add_widget(self.tituloPpal)
        self.add_widget(caja)
        self.add_widget(zonaMuestra)
        self.add_widget(footer)

    def abrirExplorador(self, obj):
        self.appExplorador=ExploradorApp(self, self.cerrar_popup)
        contenido=self.appExplorador.build()
        self._popup = Popup(title="Cargar archivo", content=contenido,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def cerrar_popup(self, obj):
        try:
            self.ruta=self.appExplorador.rutaCompleta
        except:
            self.ruta=None
        self._popup.dismiss()

    def mostrarArchivo(self, obj):
        try:
            print(self.ruta)
        except:
            pass

    def cargarArchivo(self, obj):
        try:
            print(self.ruta)
        except:
            pass
        else:
            tupla=func.cargarPrograma(self.ruta, self.posDispMem, self.vectorMemoria, self.omitirLineasGlobal, self.listaProgramas)
            if tupla==False:
                pass
            else:
                __, self.vectorMemoria, self.posDispMem, self.omitirLineasGlobal, self.listaProgramas=tupla

            self.programaActual=len(self.listaProgramas)-1
            print(self.listaProgramas)

            self.seccionInstrucciones.clear_widgets()
            self.seccionInstrucciones.__init__(self)

            self.seccionVariables.clear_widgets()
            self.seccionVariables.__init__(self)

            self.seccionEtiquetas.clear_widgets()
            self.seccionEtiquetas.__init__(self)

            self.seccionMemoria.clear_widgets()
            self.seccionMemoria.__init__(self)


class CHMaquinaApp(App):

    def build(self):
        Window.clearcolor=(26/255, 28/255, 82/255, 0.8)
        return VentanaPrincipal()

if __name__ == '__main__':
    CHMaquinaApp().run()