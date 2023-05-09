from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

from ventanasDisenos.mensajeError import *

class VentanaLectura(GridLayout):
    def __init__(self, appPrincipal, appLector, cancelar, tipoVar, **kwargs):
        super(VentanaLectura, self).__init__(**kwargs)
        self.rows=3
        self.padding=[30,10]

        self.appPrincipal=appPrincipal
        self.appLector=appLector
        self.cancelar=cancelar
        self.tipoVarLeida=tipoVar
        self.valorLeido=None
        
        self.titulo=Label(text="[b]Leer dato[/b]", markup=True, size_hint_y=0.25, height=100, font_size="35sp")
        self.add_widget(self.titulo)
        
        self.cajaTexto=TextInput(text="", size_hint_y=0.4, padding=[12,12])
        self.add_widget(self.cajaTexto)
        
        botones=GridLayout(cols=2, spacing=20, height=30, size_hint_y=0.2, padding=[10,12])
        boton1=Button(text="Aceptar")
        boton1.bind(on_release=self.verificarTextoVar)
        botones.add_widget(boton1)
        self.add_widget(botones)

    def verificarTextoVar(self, obj):
        texto=self.cajaTexto.text
        try:
            if self.tipoVarLeida=="IP100":
                try:
                    self.valorLeido=int(texto)
                    if self.valorLeido<0 or self.valorLeido>100:
                        raise ValueError("Error de lectura")
                except ValueError:
                    self.valorLeido=None
            elif self.tipoVarLeida=="C":
                try:
                    self.valorLeido=str(texto)
                except ValueError:
                    self.valorLeido=None
            elif self.tipoVarLeida=="I" or self.tipoVarLeida=="L":
                try:
                    self.valorLeido=int(texto)
                    if self.tipoVarLeida=="L" and (self.valorLeido!=0 or self.valorLeido!=1):
                        self.valorLeido=None
                except ValueError:
                    self.valorLeido=None
            elif self.tipoVarLeida=="R":
                try:
                    self.valorLeido=float(texto)
                except ValueError:
                    self.valorLeido=None
            else:
                self.valorLeido=None
        except AttributeError as error:
            self.abrirError(f"Error en la lectura: {error}")
        else:
            if self.valorLeido!=None:
                print(f"Leído con éxito: {self.valorLeido}")
                self.cancelar(None)
            else:
                self.abrirError("Error en la lectura")


    def abrirError(self, mensaje):
        self.appError=MensajeErrorApp(self, self.cerrar_Error, mensaje)
        contenido=self.appError.build()
        self._popup = Popup(title="Error", content=contenido,
                            size_hint=(0.4, 0.4))
        self._popup.open()

    def cerrar_Error(self, obj):
        self._popup.dismiss()


class LecturaValorApp(App):

    def __init__(self, appPrincipal, cancelar, tipoVar,**kwargs):
        super(LecturaValorApp,self).__init__(**kwargs)
        self.appPrincipal=appPrincipal
        self.cancelar=cancelar
        self.tipoVar=tipoVar

    def build(self):

        self.ventana=VentanaLectura(self.appPrincipal, self, self.cancelar, self.tipoVar)

        self.ventana.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.ventana.canvas.before:
            Color(31/255, 6/255, 6/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.ventana.size, pos=self.ventana.pos)
        return self.ventana

    def _actualizar_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    LecturaValorApp(None, None).run()