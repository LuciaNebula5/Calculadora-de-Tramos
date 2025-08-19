'''==================================================================================
Created by @Lucía
Produced by Nebula Studios
==================================================================================='''



from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import datetime, timedelta
import re

# ================== CONFIGURACIÓN DE APARIENCIA ==================
# Puedes modificar estos valores para cambiar la apariencia de la app

# COLORES (formato RGBA: Red, Green, Blue, Alpha - valores entre 0 y 1)
COLOR_FONDO = (0.1, 0.1, 0.15, 1)          # Fondo principal (azul oscuro)
COLOR_BOTON = (0.2, 0.6, 1, 1)             # Botón principal (azul)
COLOR_BOTON_HOVER = (0.3, 0.7, 1, 1)       # Botón al presionar (azul claro)
COLOR_TEXTO_PRINCIPAL = (1, 1, 1, 1)       # Texto principal (blanco)
COLOR_TEXTO_SECUNDARIO = (0.8, 0.8, 0.8, 1)# Texto secundario (gris claro)
COLOR_INPUT = (0.2, 0.2, 0.25, 1)          # Fondo de campos de texto
COLOR_INPUT_TEXTO = (1, 1, 1, 1)           # Texto en campos

# TAMAÑOS
TITULO_TAMAÑO = 24                          # Tamaño del título principal
TEXTO_TAMAÑO = 16                           # Tamaño del texto normal
INPUT_ALTURA = 45                           # Altura de campos de texto
BOTON_ALTURA = 55                           # Altura del botón
ESPACIADO = 15                              # Espaciado entre elementos
PADDING = 25                                # Margen exterior

# FUENTES Y ESTILOS
TITULO_NEGRITA = True                       # Si el título va en negrita
ESQUINAS_REDONDEADAS = True                 # Si quieres esquinas redondeadas (experimental)

# ================================================================

class CalculadoraTramosApp(App):
    def build(self):
        self.title = "Calculadora de Tramos v1.0"
        
        # Layout principal con colores personalizables
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=PADDING, 
            spacing=ESPACIADO
        )
        
        # Aplicar color de fondo
        from kivy.graphics import Color, Rectangle
        with main_layout.canvas.before:
            Color(*COLOR_FONDO)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Título
        title = Label(
            text='Calculadora de Tramos de Fechas',
            size_hint_y=None,
            height=60,
            font_size=TITULO_TAMAÑO,
            bold=TITULO_NEGRITA,
            color=COLOR_TEXTO_PRINCIPAL
        )
        main_layout.add_widget(title)
        
        # Instrucciones
        instrucciones = Label(
            text='Ingresa las fechas para calcular los tramos',
            size_hint_y=None,
            height=30,
            font_size=14,
            color=COLOR_TEXTO_SECUNDARIO
        )
        main_layout.add_widget(instrucciones)
        
        # Fecha inicial
        fecha_inicial_label = Label(
            text='Fecha inicial (DD/MM/AAAA):',
            size_hint_y=None,
            height=35,
            font_size=TEXTO_TAMAÑO,
            color=COLOR_TEXTO_PRINCIPAL,
            halign='left'
        )
        fecha_inicial_label.bind(size=fecha_inicial_label.setter('text_size'))
        main_layout.add_widget(fecha_inicial_label)
        
        self.fecha_inicial_input = TextInput(
            hint_text='Ej: 01/01/2024',
            size_hint_y=None,
            height=INPUT_ALTURA,
            multiline=False,
            background_color=COLOR_INPUT,
            foreground_color=COLOR_INPUT_TEXTO,
            font_size=TEXTO_TAMAÑO
        )
        main_layout.add_widget(self.fecha_inicial_input)
        
        # Fecha final
        fecha_final_label = Label(
            text='Fecha final (DD/MM/AAAA):',
            size_hint_y=None,
            height=35,
            font_size=TEXTO_TAMAÑO,
            color=COLOR_TEXTO_PRINCIPAL,
            halign='left'
        )
        fecha_final_label.bind(size=fecha_final_label.setter('text_size'))
        main_layout.add_widget(fecha_final_label)
        
        self.fecha_final_input = TextInput(
            hint_text='Ej: 31/01/2024',
            size_hint_y=None,
            height=INPUT_ALTURA,
            multiline=False,
            background_color=COLOR_INPUT,
            foreground_color=COLOR_INPUT_TEXTO,
            font_size=TEXTO_TAMAÑO
        )
        main_layout.add_widget(self.fecha_final_input)
        
        # Botón calcular
        calcular_btn = Button(
            text='Calcular Tramos',
            size_hint_y=None,
            height=BOTON_ALTURA,
            background_color=COLOR_BOTON,
            font_size=TEXTO_TAMAÑO + 2,
            bold=True
        )
        calcular_btn.bind(on_press=self.calcular_tramos)
        main_layout.add_widget(calcular_btn)
        
        # Botón limpiar
        limpiar_btn = Button(
            text=' Limpiar',
            size_hint_y=None,
            height=40,
            background_color=(0.6, 0.6, 0.6, 1),
            font_size=TEXTO_TAMAÑO - 2
        )
        limpiar_btn.bind(on_press=self.limpiar_campos)
        main_layout.add_widget(limpiar_btn)
        
        # Área de resultados
        self.resultado_label = Label(
            text='Los resultados aparecerán aquí...',
            text_size=(None, None),
            valign='top',
            markup=True,
            font_size=TEXTO_TAMAÑO - 1,
            color=COLOR_TEXTO_SECUNDARIO
        )
        main_layout.add_widget(self.resultado_label)
        
        # Layout para la versión (abajo a la derecha)
        version_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        
        # Espacio en blanco a la izquierda
        version_layout.add_widget(Label())
        
        # Etiqueta de versión
        version_label = Label(
            text='v1.0',
            size_hint_x=None,
            width=50,
            font_size=12,
            color=(0.5, 0.5, 0.5, 1),
            halign='right'
        )
        version_label.bind(size=version_label.setter('text_size'))
        version_layout.add_widget(version_label)
        
        main_layout.add_widget(version_layout)
        
        return main_layout
    
    def _update_rect(self, instance, value):
        """Actualiza el fondo cuando cambia el tamaño"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def limpiar_campos(self, instance):
        """Limpia todos los campos"""
        self.fecha_inicial_input.text = ""
        self.fecha_final_input.text = ""
        self.resultado_label.text = 'Los resultados aparecerán aquí...\n\n💡 Tip: El cálculo descarta los primeros 13 días\ny luego divide el resto en tramos.'
        self.resultado_label.color = COLOR_TEXTO_SECUNDARIO
    
    def validar_fecha(self, fecha_str):
        """Valida que la fecha tenga el formato correcto DD/MM/AAAA"""
        patron = r'^(\d{1,2})/(\d{1,2})/(\d{4})$'
        match = re.match(patron, fecha_str)
        
        if not match:
            return None
            
        dia, mes, año = map(int, match.groups())
        
        try:
            fecha = datetime(año, mes, dia)
            return fecha
        except ValueError:
            return None
    
    def mostrar_error(self, mensaje):
        """Muestra un popup con mensaje de error"""
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        error_label = Label(
            text=f" {mensaje}", 
            text_size=(280, None), 
            halign='center',
            font_size=TEXTO_TAMAÑO,
            color=(1, 0.3, 0.3, 1)
        )
        content.add_widget(error_label)
        
        close_btn = Button(
            text='Cerrar', 
            size_hint_y=None, 
            height=45,
            background_color=COLOR_BOTON,
            font_size=TEXTO_TAMAÑO
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Error',
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=False,
            background_color=COLOR_FONDO
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def calcular_tramos(self, instance):
        """Función principal que calcula los tramos"""
        fecha_inicial_str = self.fecha_inicial_input.text.strip()
        fecha_final_str = self.fecha_final_input.text.strip()
        
        # Validar que se ingresaron fechas
        if not fecha_inicial_str or not fecha_final_str:
            self.mostrar_error("Por favor, ingresa ambas fechas.")
            return
        
        # Validar formato de fechas
        fecha_inicial = self.validar_fecha(fecha_inicial_str)
        fecha_final = self.validar_fecha(fecha_final_str)
        
        if fecha_inicial_str is None:
            self.mostrar_error("Fecha inicial inválida. Usa el formato DD/MM/AAAA")
            return
            
        if fecha_final is None:
            self.mostrar_error("Fecha final inválida. Usa el formato DD/MM/AAAA")
            return
        
        # Validar que la fecha final sea posterior a la inicial
        if fecha_final <= fecha_inicial:
            self.mostrar_error("La fecha final debe ser posterior a la fecha inicial.")
            return
        
        # Calcular días totales
        dias_totales = (fecha_final - fecha_inicial).days
        
        # Verificar que hay al menos 14 días (13 para descartar + 1 mínimo)
        if dias_totales < 14:
            self.mostrar_error("Debe haber al menos 14 días entre las fechas\n(13 días a descartar + al menos 1 día más)")
            return
        
        # Descartar los primeros 13 días
        fecha_inicio_tramos = fecha_inicial + timedelta(days=13)
        dias_restantes = (fecha_final - fecha_inicio_tramos).days
        
        # Calcular tramos
        if dias_restantes <= 7:
            # Solo TRAMO 1
            tramo1_inicio = fecha_inicio_tramos
            tramo1_fin = fecha_final
            tramo1_dias = dias_restantes
            
            resultado = f"""[b][size=18] RESULTADOS:[/size][/b]

[color=ff6b6b] Días descartados:[/color] [b]{(fecha_inicio_tramos - fecha_inicial).days} días[/b]
[color=888888][size=14]({fecha_inicial.strftime('%d/%m/%Y')} - {(fecha_inicio_tramos - timedelta(days=1)).strftime('%d/%m/%Y')})[/size][/color]

[color=4ecdc4][b][size=16] TRAMO 1:[/b][/color] [b]{tramo1_dias} días[/b]
[color=888888][size=14]({tramo1_inicio.strftime('%d/%m/%Y')} - {tramo1_fin.strftime('%d/%m/%Y')})[/size][/color]

[color=95e1d3][size=14] No hay TRAMO 2[/size][/color]
[color=888888][size=12](El TRAMO 1 tiene 7 días o menos)[/size][/color]"""
        
        else:
            # TRAMO 1 y TRAMO 2
            tramo1_inicio = fecha_inicio_tramos
            tramo1_fin = fecha_inicio_tramos + timedelta(days=6)  # 7 días (0-6)
            tramo1_dias = 7
            
            tramo2_inicio = tramo1_fin + timedelta(days=1)
            tramo2_fin = fecha_final
            tramo2_dias = (tramo2_fin - tramo2_inicio).days
            
            resultado = f"""[b][size=18] RESULTADOS:[/size][/b]

[color=ff6b6b] Días descartados:[/color] [b]{(fecha_inicio_tramos - fecha_inicial).days} días[/b]
[color=888888][size=14]({fecha_inicial.strftime('%d/%m/%Y')} - {(fecha_inicio_tramos - timedelta(days=1)).strftime('%d/%m/%Y')})[/size][/color]

[color=4ecdc4][b][size=16] TRAMO 1:[/b][/color] [b]{tramo1_dias} días[/b]
[color=888888][size=14]({tramo1_inicio.strftime('%d/%m/%Y')} - {tramo1_fin.strftime('%d/%m/%Y')})[/size][/color]

[color=feca57][b][size=16] TRAMO 2:[/b][/color] [b]{tramo2_dias} días[/b]
[color=888888][size=14]({tramo2_inicio.strftime('%d/%m/%Y')} - {tramo2_fin.strftime('%d/%m/%Y')})[/size][/color]"""
        
        # Actualizar el resultado en la interfaz
        self.resultado_label.text = resultado
        # Hacer que el texto se ajuste al ancho de la pantalla para móviles
        self.resultado_label.bind(width=lambda *x: self.resultado_label.setter('text_size')(self.resultado_label, (self.resultado_label.width, None)))
        self.resultado_label.color = COLOR_TEXTO_PRINCIPAL

def main():
    """Función principal para BeeWare"""
    app = CalculadoraTramosApp()
    app.run()

if __name__ == '__main__':
    main()