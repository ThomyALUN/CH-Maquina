from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from RecuadroImagen import *

import funciones as func

# Contiene las clases que definen las secciones principales de la interfaz gráfica

sizeFontScroll="14sp"

class SeccionInstrucciones(GridLayout, ActualizaRect):

    def __init__(self, app, **kwargs):
        super(SeccionInstrucciones, self).__init__(**kwargs)
        self.rows=2
        self.app=app
        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(89/255, 14/255, 100/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.resetSeccion()  

    def resetSeccion(self):
        self.clear_widgets()

        self.titulo=GridLayout(cols=3, size_hint_y=0.12)

        etiqueta1=Label(text="[b]Sig[/b]", markup=True, size_hint_x=0.2)
        etiqueta2=Label(text="[b]Pos[/b]", markup=True, size_hint_x=0.35)
        etiqueta3=Label(text="[b]Instr[/b]", markup=True, size_hint_x=0.45)
        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)        
        self.titulo.add_widget(etiqueta3)  

        if self.app.listaProgramas==[]:
            self.scroll=VacioInstrucciones()
        else:
            self.scroll=ScrollInstrucciones(self.app)

        self.add_widget(self.titulo)
        self.add_widget(self.scroll) 


class VacioInstrucciones(BoxLayout, ActualizaRect):

    def __init__(self, **kwargs):
        super(VacioInstrucciones, self).__init__(**kwargs)

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(134/255, 134/255, 135/255, 0.41)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.add_widget(Label(text="- - -", size_hint_x=0.2))
        self.add_widget(Label(text="- - -", size_hint_x=0.35))
        self.add_widget(Label(text="- - -", size_hint_x=0.45))


class ScrollInstrucciones(ScrollView, ActualizaRect):

    def __init__(self, app, **kwargs):
        super(ScrollInstrucciones, self).__init__(**kwargs)

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(134/255, 134/255, 135/255, 0.41)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.app=app
        self.listaSigIns=[]
        vectorMemoria=app.vectorMemoria
        programaActual=app.programaActual
        columnaInstrucciones=GridLayout(cols=3, spacing=5, size_hint_y=None)
        # Permite que se mueva a través de todos los datos
        columnaInstrucciones.bind(minimum_height=columnaInstrucciones.setter('height'))

        self.limites=app.listaProgramas[programaActual][0]
        
        for pos in range(self.limites[0],self.limites[1]):
            instruccion=vectorMemoria[pos]
            mensaje1=""
            if pos==self.app.apuntador:
                mensaje1+="->"
            mensaje2=f"{func.agregarCeros(pos,4)}"
            mensaje3=f"{instruccion}"
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, width=50, size_hint_x=0.2, font_size=sizeFontScroll)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, width=100, size_hint_x=0.35, font_size=sizeFontScroll)
            etiqueta3 = Label(text=str(mensaje3), size_hint_y=None, size_hint_x=0.45, text_size=(100, None), font_size=sizeFontScroll)
            self.listaSigIns.append(etiqueta1)
            columnaInstrucciones.add_widget(etiqueta1)
            columnaInstrucciones.add_widget(etiqueta2)
            columnaInstrucciones.add_widget(etiqueta3)
        self.add_widget(columnaInstrucciones)


    def actualizarIns(self):
        for pos in range(self.limites[0],self.limites[1]):
            mensaje=""
            if pos==self.app.apuntador:
                mensaje+="->"
            self.listaSigIns[pos-self.limites[0]].text=mensaje          #Se cambia el valor de cada etiqueta que representa el espacio de instrucción siguiente


class SeccionVariables(GridLayout, ActualizaRect):

    def __init__(self, app, **kwargs):
        super(SeccionVariables, self).__init__(**kwargs)
        self.rows=2
        self.app=app

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(89/255, 14/255, 100/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.resetSeccion()

    def resetSeccion(self):
        self.clear_widgets()

        self.titulo=GridLayout(cols=2, size_hint_y=0.24)

        etiqueta1=Label(text="[b]Posición[/b]", markup=True)
        etiqueta2=Label(text="[b]Variable[/b]", markup=True)
        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)

        if self.app.listaProgramas==[]:
            self.scroll=VacioVarEtq()
        else:
            self.scroll=ScrollVariables(self.app)

        self.add_widget(self.titulo)
        self.add_widget(self.scroll)


class ScrollVariables(ScrollView, ActualizaRect):

    def __init__(self, app, **kwargs):
        super(ScrollVariables, self).__init__(**kwargs)

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(134/255, 134/255, 135/255, 0.41)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

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
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, height=40, width=100, font_size=sizeFontScroll)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, height=40, width=100, font_size=sizeFontScroll)
            columnaVariables.add_widget(etiqueta1)
            columnaVariables.add_widget(etiqueta2)
        self.add_widget(columnaVariables)


class SeccionEtiquetas(GridLayout, ActualizaRect):

    def __init__(self, app, **kwargs):
        super(SeccionEtiquetas, self).__init__(**kwargs)
        self.rows=2
        self.app=app

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(89/255, 14/255, 100/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.resetSeccion()

    def resetSeccion(self):
        self.clear_widgets()

        self.titulo=GridLayout(cols=2, size_hint_y=0.24)

        etiqueta1=Label(text="[b]Posición[/b]", markup=True)
        etiqueta2=Label(text="[b]Etiqueta[/b]", markup=True)

        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)

        if self.app.listaProgramas==[]:
            self.scroll=VacioVarEtq()
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
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, height=40, width=100, font_size=sizeFontScroll)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, height=40, width=100, font_size=sizeFontScroll)
            columnaEtiquetas.add_widget(etiqueta1)
            columnaEtiquetas.add_widget(etiqueta2)
        self.add_widget(columnaEtiquetas)


class VacioVarEtq(BoxLayout, ActualizaRect):

    def __init__(self, **kwargs):
        super(VacioVarEtq, self).__init__(**kwargs)

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(134/255, 134/255, 135/255, 0.41)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.add_widget(Label(text="- - -"))
        self.add_widget(Label(text="- - -"))


class SeccionResultados(GridLayout):

    def __init__(self, app, **kwargs):
        super(SeccionResultados, self).__init__(**kwargs)
        self.rows=2
        resultados=GridLayout(rows=2)
        self.app=app

        pantalla=GridLayout(rows=2, size_hint_y=0.5)
        etiqueta1=Label(text="[b]PANTALLA[/b]",size_hint_y=0.2, markup=True)
        cajaTexto1=GridLayout(rows=1,padding=[20,10])
        espacioInteraccion=RecuadroImagen("...",'imagenes/pantalla.png')
        self.textoPantalla=espacioInteraccion.etiqueta
        cajaTexto1.add_widget(espacioInteraccion)

        pantalla.add_widget(etiqueta1)
        pantalla.add_widget(cajaTexto1)

        impresora=GridLayout(rows=2, size_hint_y=0.5)
        etiqueta2=Label(text="[b]IMPRESORA[/b]",size_hint_y=0.2, markup=True)
        cajaTexto2=GridLayout(rows=1,padding=[20,10])
        espacioImpresora=RecuadroImagen("...",'imagenes/impresora.png')
        self.textoImpreso=espacioImpresora.etiqueta
        cajaTexto2.add_widget(espacioImpresora)
        
        impresora.add_widget(etiqueta2)
        impresora.add_widget(cajaTexto2)

        resultados.add_widget(pantalla)
        resultados.add_widget(impresora)

        self.add_widget(resultados)


class SeccionMemoria(GridLayout, ActualizaRect):

    def __init__(self, app, **kwargs):
        super(SeccionMemoria, self).__init__(**kwargs)
        self.rows=2
        self.app=app

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(89/255, 14/255, 100/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.titulo=GridLayout(cols=2, size_hint_y=0.12)

        etiqueta1=Label(text="[b]Posición[/b]", markup=True, size_hint_x=0.45)
        etiqueta2=Label(text="[b]Memoria[/b]", markup=True, size_hint_x=0.55)

        self.titulo.add_widget(etiqueta1)
        self.titulo.add_widget(etiqueta2)
        self.scroll=ScrollMemoria(self.app)

        self.add_widget(self.titulo)
        self.add_widget(self.scroll)
    
    def setScroll(self):
        self.scroll=ScrollMemoria(self.app)


class ScrollMemoria(ScrollView, ActualizaRect):

    def __init__(self, app, **kwargs):
        super(ScrollMemoria, self).__init__(**kwargs)

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(134/255, 134/255, 135/255, 0.41)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        columnaMemoria=GridLayout(cols=2, spacing=5, size_hint_y=None)
        # Permite que se mueva a través de todos los datos
        columnaMemoria.bind(minimum_height=columnaMemoria.setter('height'))
        self.listaDatosMem=[]
        self.app=app

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
            etiqueta1 = Label(text=str(mensaje1), size_hint_y=None, text_size=(60, None), font_size=sizeFontScroll)
            etiqueta2 = Label(text=str(mensaje2), size_hint_y=None, text_size=(100, None), font_size=sizeFontScroll)
            columnaMemoria.add_widget(etiqueta1)
            columnaMemoria.add_widget(etiqueta2)
            self.listaDatosMem.append(etiqueta2)
        self.add_widget(columnaMemoria)
    
    def actualizarDatosMem(self):
        for pos, direccionMem in enumerate(self.app.vectorMemoria):
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
            self.listaDatosMem[pos].text=mensaje2
