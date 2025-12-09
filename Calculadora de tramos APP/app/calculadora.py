"""
By @Lucix
Produced by: Nebula Studio
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import re

from config.colores import *
from config.tamano import *
from textos.es import TEXTOS


class CalculadoraLayout(BoxLayout):
    """Layout principal de la calculadora"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = PADDING
        self.spacing = ESPACIADO
        
        # Aplicar fondo
        with self.canvas.before:
            Color(*COLOR_FONDO)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect, pos=self.update_rect)
        
        self.build_ui()
    
    def build_ui(self):
        """Construye toda la interfaz"""
        
        # ========== TÍTULO ==========
        titulo = Label(
            text=TEXTOS['titulo'],
            size_hint_y=None,
            height=60,
            font_size=TITULO_TAMANO,
            bold=TITULO_NEGRITA,
            color=COLOR_TEXTO_PRINCIPAL
        )
        self.add_widget(titulo)
        
        # ========== INSTRUCCIONES ==========
        instrucciones = Label(
            text=TEXTOS['instrucciones'],
            size_hint_y=None,
            height=30,
            font_size=14,
            color=COLOR_TEXTO_SECUNDARIO
        )
        self.add_widget(instrucciones)
        
        # ========== FECHA INICIAL ==========
        fecha_inicial_label = Label(
            text=TEXTOS['fecha_inicial'],
            size_hint_y=None,
            height=35,
            font_size=TEXTO_TAMANO,
            color=COLOR_TEXTO_PRINCIPAL,
            halign='left'
        )
        fecha_inicial_label.bind(size=fecha_inicial_label.setter('text_size'))
        self.add_widget(fecha_inicial_label)
        
        self.fecha_inicial_input = TextInput(
            hint_text='Ej: 01012024',
            size_hint_y=None,
            height=INPUT_ALTURA,
            multiline=False,
            background_color=COLOR_INPUT,
            foreground_color=COLOR_INPUT_TEXTO,
            font_size=TEXTO_TAMANO
        )
        self.add_widget(self.fecha_inicial_input)
        
        # ========== FECHA FINAL ==========
        fecha_final_label = Label(
            text=TEXTOS['fecha_final'],
            size_hint_y=None,
            height=35,
            font_size=TEXTO_TAMANO,
            color=COLOR_TEXTO_PRINCIPAL,
            halign='left'
        )
        fecha_final_label.bind(size=fecha_final_label.setter('text_size'))
        self.add_widget(fecha_final_label)
        
        self.fecha_final_input = TextInput(
            hint_text='Ej: 31012024',
            size_hint_y=None,
            height=INPUT_ALTURA,
            multiline=False,
            background_color=COLOR_INPUT,
            foreground_color=COLOR_INPUT_TEXTO,
            font_size=TEXTO_TAMANO
        )
        self.add_widget(self.fecha_final_input)
        
        # ========== BOTÓN CALCULAR ==========
        calcular_btn = Button(
            text=TEXTOS['calcular'],
            size_hint_y=None,
            height=BOTON_ALTURA,
            background_color=COLOR_BOTON,
            font_size=TEXTO_TAMANO,
            bold=True
        )
        calcular_btn.bind(on_press=self.calcular_tramos)
        self.add_widget(calcular_btn)
        
        # ========== BOTÓN LIMPIAR ==========
        limpiar_btn = Button(
            text=TEXTOS['limpiar'],
            size_hint_y=None,
            height=40,
            background_color=(0.6, 0.6, 0.6, 1),
            font_size=TEXTO_TAMANO - 2
        )
        limpiar_btn.bind(on_press=self.limpiar_campos)
        self.add_widget(limpiar_btn)
        
        # ========== ÁREA DE RESULTADOS ==========
        self.resultado_label = Label(
            text=TEXTOS['resultado_inicial'],
            size_hint_y=None,
            height=RESULTADO_ALTURA,        # ← 350px+ de altura
            text_size=(None, None),
            valign='top',
            markup=True,
            font_size=TEXTO_TAMANO - 1,
            color=COLOR_TEXTO_SECUNDARIO
        )
        self.add_widget(self.resultado_label)
        
        # ========== VERSIÓN (abajo a la derecha) ==========
        version_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        version_layout.add_widget(Label())  # Espacio vacío a la izquierda
        
        version_label = Label(
            text=TEXTOS['version'],
            size_hint_x=None,
            width=50,
            font_size=12,
            color=(0.5, 0.5, 0.5, 1),
            halign='right'
        )
        version_label.bind(size=version_label.setter('text_size'))
        version_layout.add_widget(version_label)
        
        self.add_widget(version_layout)
    
    def update_rect(self, instance, value):
        """Actualiza el rectángulo de fondo cuando cambia el tamaño"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def limpiar_campos(self, instance):
        """Limpia todos los campos de entrada"""
        self.fecha_inicial_input.text = ''
        self.fecha_final_input.text = ''
        self.resultado_label.text = TEXTOS['resultado_inicial']
        self.resultado_label.color = COLOR_TEXTO_SECUNDARIO
    
    def validar_fecha(self, fecha_str):
        """
        Valida que la fecha tenga el formato correcto (DDMMAAAA)
        Retorna objeto datetime o None si es inválida
        """
        patron = r'(\d{2})(\d{2})(\d{4})'
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
            text=f'❌ {mensaje}',
            text_size=(280, None),
            halign='center',
            font_size=TEXTO_TAMANO,
            color=(1, 0.3, 0.3, 1)
        )
        content.add_widget(error_label)
        
        close_btn = Button(
            text=TEXTOS['limpiar'],
            size_hint_y=None,
            height=45,
            background_color=COLOR_BOTON,
            font_size=TEXTO_TAMANO
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
        
        # ========== VALIDACIÓN: Campos vacíos ==========
        if not fecha_inicial_str or not fecha_final_str:
            self.mostrar_error(TEXTOS['error_fechas'])
            return
        
        # ========== VALIDACIÓN: Formato de fechas ==========
        fecha_inicial = self.validar_fecha(fecha_inicial_str)
        fecha_final = self.validar_fecha(fecha_final_str)
        
        if fecha_inicial is None:
            self.mostrar_error(TEXTOS['error_formato'] + ' (Fecha inicial)')
            return
        
        if fecha_final is None:
            self.mostrar_error(TEXTOS['error_formato'] + ' (Fecha final)')
            return
        
        # ========== VALIDACIÓN: Fecha final > fecha inicial ==========
        if fecha_final <= fecha_inicial:
            self.mostrar_error(TEXTOS['error_logica'])
            return
        
        # ========== VALIDACIÓN: Mínimo 14 días ==========
        dias_totales = (fecha_final - fecha_inicial).days
        
        if dias_totales < 14:
            self.mostrar_error(TEXTOS['error_dias'])
            return
        
        # ========== CÁLCULO: Descartar 13 días iniciales ==========
        fecha_inicio_tramos = fecha_inicial + timedelta(days=13)
        dias_restantes = (fecha_final - fecha_inicio_tramos).days
        
        # ========== LÓGICA: Solo TRAMO 1 (7 días o menos) ==========
        if dias_restantes <= 7:
            tramo1_inicio = fecha_inicio_tramos
            tramo1_fin = fecha_final
            tramo1_dias = dias_restantes
            
            resultado = (
                f'[size=18][b][color=ff6b6b]RESULTADOS[/color][/b][/size]\n\n'
                f'[color=ff6b6b][b]Días descartados:[/b][/color] '
                f'[b]{(fecha_inicio_tramos - fecha_inicial).days} días[/b] '
                f'[color=888888][size=14](Del {fecha_inicial.strftime("%d/%m/%Y")} '
                f'al {(fecha_inicio_tramos - timedelta(days=1)).strftime("%d/%m/%Y")})[/size][/color]\n\n'
                f'[color=4ecdc4][size=16][b]TRAMO 1[/b][/size][/color]\n'
                f'[b]{tramo1_dias} días[/b] '
                f'[color=888888][size=14](Del {tramo1_inicio.strftime("%d/%m/%Y")} '
                f'al {tramo1_fin.strftime("%d/%m/%Y")})[/size][/color]\n\n'
                f'[color=95e1d3][size=14]No hay TRAMO 2[/size][/color] '
                f'[color=888888][size=12](Menos de 8 días restantes)[/size][/color]'
            )
        
        # ========== LÓGICA: TRAMO 1 + TRAMO 2 (más de 7 días) ==========
        else:
            tramo1_inicio = fecha_inicio_tramos
            tramo1_fin = fecha_inicio_tramos + timedelta(days=6)  # 7 días (0-6)
            tramo1_dias = 7
            
            tramo2_inicio = tramo1_fin + timedelta(days=1)
            tramo2_fin = fecha_final
            tramo2_dias = (tramo2_fin - tramo2_inicio).days
            
            resultado = (
                f'[size=18][b][color=ff6b6b]RESULTADOS[/color][/b][/size]\n\n'
                f'[color=ff6b6b][b]Días descartados:[/b][/color] '
                f'[b]{(fecha_inicio_tramos - fecha_inicial).days} días[/b] '
                f'[color=888888][size=14](Del {fecha_inicial.strftime("%d/%m/%Y")} '
                f'al {(fecha_inicio_tramos - timedelta(days=1)).strftime("%d/%m/%Y")})[/size][/color]\n\n'
                f'[color=4ecdc4][size=16][b]TRAMO 1[/b][/size][/color]\n'
                f'[b]{tramo1_dias} días[/b] '
                f'[color=888888][size=14](Del {tramo1_inicio.strftime("%d/%m/%Y")} '
                f'al {tramo1_fin.strftime("%d/%m/%Y")})[/size][/color]\n\n'
                f'[color=feca57][size=16][b]TRAMO 2[/b][/size][/color]\n'
                f'[b]{tramo2_dias} días[/b] '
                f'[color=888888][size=14](Del {tramo2_inicio.strftime("%d/%m/%Y")} '
                f'al {tramo2_fin.strftime("%d/%m/%Y")})[/size][/color]'
            )
        
        # ========== ACTUALIZAR RESULTADO ==========
        self.resultado_label.text = resultado
        self.resultado_label.bind(
            width=lambda x: self.resultado_label.setter('text_size')(
                self.resultado_label, (self.resultado_label.width, None)
            )
        )
        self.resultado_label.color = COLOR_TEXTO_PRINCIPAL
