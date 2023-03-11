from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, Rectangle, RoundedRectangle
import os

class VentanaExplorador(GridLayout):
    def __init__(self, appPrincipal, appExplorador, cancelar,**kwargs):
        self.rows=3
        self.padding=[30,10]
        super(VentanaExplorador, self).__init__(**kwargs)

        self.appPrincipal=appPrincipal
        self.appExplorador=appExplorador
        self.cancelar=cancelar
        self.rutaCompleta=None
        
        self.titulo=Label(text="[b]Explorador de archivos[/b]", markup=True, size_hint_y=0.1, height=100, font_size="40sp")
        self.add_widget(self.titulo)
        
        self.explorador=ExploradorArchivos(size_hint_y=0.8)
        self.add_widget(self.explorador)
        
        botones=GridLayout(cols=2, spacing=150, height=30, size_hint_y=0.1, padding=[50,12])
        boton1=Button(text="Aceptar")
        boton1.bind(on_release=self.cargarArchivo)
        boton2=Button(text="Cancelar")
        boton2.bind(on_release=self.cancelar)
        botones.add_widget(boton1)
        botones.add_widget(boton2)
        self.add_widget(botones)

    def mostrarRuta(self):
        print(self.explorador.path, self.explorador.selection)

    def cargarArchivo(self,obj):
        path=self.explorador.path, 
        nombreArchivo=self.explorador.selection
        try:
            rutaCompleta=os.path.join(path[0], nombreArchivo[0])
            with open(rutaCompleta) as archivo:
                print(archivo.read())
            self.rutaCompleta=rutaCompleta
            self.appExplorador.rutaCompleta=rutaCompleta
            self.cancelar(None)
        except:
            print("Archivo inválido")

    def cerrarApp(self,obj):
        print(self.rutaCompleta)
        self.appExplorador.stop()


class ExploradorArchivos(FileChooserListView):

    def __init__(self, **kwargs):
        super(ExploradorArchivos, self).__init__(**kwargs)

        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(89/255, 14/255, 100/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
    
    def _actualizar_rect(self, instance, value):
        self.rect.pos = (0,0)
        self.rect.size = instance.size


class ExploradorApp(App):

    def __init__(self, appPrincipal, cancelar, **kwargs):
        super(ExploradorApp,self).__init__(**kwargs)
        self.appPrincipal=appPrincipal
        self.cancelar=cancelar

    def build(self):

        ventana=VentanaExplorador(self.appPrincipal, self, self.cancelar)
    
        ventana.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with ventana.canvas.before:
            Color(31/255, 6/255, 6/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=ventana.size, pos=ventana.pos)
        return ventana

    def _actualizar_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    ExploradorApp(None).run()