from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Rectangle, RoundedRectangle, Color


# Contiene el método que permite actualizar la zona coloreada de una elementro gráfico
class ActualizaRect():

    def colorRectanguloPlano(self, color):
        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(color[0], color[1], color[2], color[3])  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def colorRectanguloSuave(self, color):
        self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.canvas.before:
            Color(color[0], color[1], color[2], color[3])  # colors range from 0-1 not 0-255
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)

    def _actualizar_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


class EtiquetaEstilizada(BoxLayout, ActualizaRect):
    def __init__(self, texto, color, font_size="12sp",**kwargs):
        super(EtiquetaEstilizada, self).__init__(**kwargs)
        self.colorRectanguloSuave(color)
        self.add_widget(Label(text=texto, font_size=font_size))


class RecuadroImagen(GridLayout, ActualizaRect):
    def __init__(self, texto, ruta, **kwargs):
        super(RecuadroImagen, self).__init__(**kwargs)
        self.rows=2
        bg_image = Image(source=ruta).texture

        # Creamos la instancia de la imagen de fondo
        with self.canvas:
            self.rect = Rectangle(texture=bg_image, pos=self.pos, size=self.size)
        self.bind(pos=self._actualizar_rect, size=self._actualizar_rect)
        
        self.etiqueta=Label(text=texto, font_size="18sp")
            
        self.add_widget(self.etiqueta)


class MyApp(App):
    def build(self):
        return RecuadroImagen("Hola mundo",'imagenes/impresora.png')

if __name__ == '__main__':
    MyApp().run()