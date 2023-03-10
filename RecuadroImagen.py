from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Rectangle, Color


# Contiene el método que permite actualizar la zona coloreada de una elementro gráfico
class ActualizaRect():
    def _actualizar_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


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