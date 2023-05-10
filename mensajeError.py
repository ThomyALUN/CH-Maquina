from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class VentanaError(GridLayout):
    def __init__(self, appPrincipal, appError, cancelar, mensaje, **kwargs):
        super(VentanaError, self).__init__(**kwargs)
        self.rows=3
        self.padding=[30,10]

        self.appPrincipal=appPrincipal
        self.appError=appError
        self.cancelar=cancelar
        self.valorLeido=None
        
        self.titulo=Label(text="[b]Error[/b]", markup=True, size_hint_y=0.25, height=100, font_size="35sp")
        self.add_widget(self.titulo)
        
        self.textoError=Label(text=mensaje, size_hint_y=0.4, padding=[12,12], text_size=(300, None))
        self.add_widget(self.textoError)
        
        botones=GridLayout(cols=2, spacing=20, height=30, size_hint_y=0.2, padding=[10,12])
        boton1=Button(text="OK")
        boton1.bind(on_release=self.cancelar)
        botones.add_widget(boton1)
        self.add_widget(botones)


class MensajeErrorApp(App):

    def __init__(self, appPrincipal, cancelar, mensaje,**kwargs):
        super(MensajeErrorApp,self).__init__(**kwargs)
        self.appPrincipal=appPrincipal
        self.cancelar=cancelar
        self.mensaje=mensaje

    def build(self):

        self.ventana=VentanaError(self.appPrincipal, self, self.cancelar, self.mensaje)

        self.ventana.bind(size=self._actualizar_rect, pos=self._actualizar_rect)

        with self.ventana.canvas.before:
            Color(31/255, 6/255, 6/255, 0.8)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=self.ventana.size, pos=self.ventana.pos)
        return self.ventana

    def _actualizar_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    MensajeErrorApp(None, None, "Index Error").run()