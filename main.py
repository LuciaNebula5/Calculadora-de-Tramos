"""
Calculadora de Tramos por Fechas - Versión Kivy
Aplicación multiplataforma (PC y Android/iOS)
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.core.window import Window
from datetime import datetime, timedelta
import calendar

# Configurar tamaño mínimo de ventana
#ACTIVAR SOLO PARA .exe y probar la app
#Window.size = (400, 700)

#Calendario Interactivo
class CalendarioPopup(Popup):
    """Popup con calendario interactivo para selección de fechas"""
    
    def __init__(self, callback, fecha_inicial=None, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.fecha_seleccionada = fecha_inicial if fecha_inicial else datetime.now()
        
        self.title = "Seleccionar Fecha"
        self.size_hint = (0.9, 0.8)
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Navegación mes/año
        nav_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        
        btn_prev_year = Button(text='<<', on_press=self.prev_year)
        btn_prev_month = Button(text='<', on_press=self.prev_month)
        
        self.label_mes_year = Label(
            text='',
            font_size='14sp',
            bold=True,
            size_hint_x=2
        )
        
        btn_next_month = Button(text='>', on_press=self.next_month)
        btn_next_year = Button(text='>>', on_press=self.next_year)
        
        nav_layout.add_widget(btn_prev_year)
        nav_layout.add_widget(btn_prev_month)
        nav_layout.add_widget(self.label_mes_year)
        nav_layout.add_widget(btn_next_month)
        nav_layout.add_widget(btn_next_year)
        
        layout.add_widget(nav_layout)
        
        # Días de la semana
        dias_semana = BoxLayout(size_hint_y=None, height=dp(40))
        for dia in ['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá', 'Do']:
            dias_semana.add_widget(Label(
                text=dia,
                font_size='14sp',
                bold=True
            ))
        layout.add_widget(dias_semana)
        
        # Grid de días del mes
        self.grid_dias = BoxLayout(orientation='vertical', spacing=dp(2))
        layout.add_widget(self.grid_dias)
        
        # Botones de acción
        botones_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        btn_hoy = Button(
            text='Hoy',
            on_press=self.seleccionar_hoy,
            background_color=(0.3, 0.7, 1, 1)
        )
        btn_cancelar = Button(
            text='Cancelar',
            on_press=self.dismiss,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        
        botones_layout.add_widget(btn_hoy)
        botones_layout.add_widget(btn_cancelar)
        
        layout.add_widget(botones_layout)
        
        self.content = layout
        self.actualizar_calendario()
    
    def actualizar_calendario(self):
        """Actualiza el calendario con el mes y año actual"""
        self.grid_dias.clear_widgets()
        
        # Actualizar título
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Sept', 'Octubre', 'Nov', 'Dic']
        self.label_mes_year.text = f"{meses[self.fecha_seleccionada.month - 1]} {self.fecha_seleccionada.year}"
        
        # Obtener días del mes
        cal = calendar.monthcalendar(self.fecha_seleccionada.year, self.fecha_seleccionada.month)
        
        for semana in cal:
            fila = BoxLayout(spacing=dp(2))
            for dia in semana:
                if dia == 0:
                    fila.add_widget(Label(text=''))
                else:
                    btn = Button(
                        text=str(dia),
                        on_press=lambda x, d=dia: self.seleccionar_dia(d)
                    )
                    
                    # Resaltar día seleccionado
                    if (dia == self.fecha_seleccionada.day and
                        datetime(self.fecha_seleccionada.year, self.fecha_seleccionada.month, dia).date() == 
                        self.fecha_seleccionada.date()):
                        btn.background_color = (0.2, 0.6, 1, 1)
                    
                    fila.add_widget(btn)
            
            self.grid_dias.add_widget(fila)
    
    def seleccionar_dia(self, dia):
        """Selecciona un día y cierra el popup"""
        self.fecha_seleccionada = datetime(
            self.fecha_seleccionada.year,
            self.fecha_seleccionada.month,
            dia
        )
        self.callback(self.fecha_seleccionada)
        self.dismiss()
    
    def seleccionar_hoy(self, instance):
        """Selecciona la fecha de hoy"""
        self.fecha_seleccionada = datetime.now()
        self.callback(self.fecha_seleccionada)
        self.dismiss()
    
    def prev_month(self, instance):
        """Mes anterior"""
        mes = self.fecha_seleccionada.month - 1
        year = self.fecha_seleccionada.year
        if mes < 1:
            mes = 12
            year -= 1
        self.fecha_seleccionada = datetime(year, mes, 1)
        self.actualizar_calendario()
    
    def next_month(self, instance):
        """Mes siguiente"""
        mes = self.fecha_seleccionada.month + 1
        year = self.fecha_seleccionada.year
        if mes > 12:
            mes = 1
            year += 1
        self.fecha_seleccionada = datetime(year, mes, 1)
        self.actualizar_calendario()
    
    def prev_year(self, instance):
        """Año anterior"""
        self.fecha_seleccionada = datetime(
            self.fecha_seleccionada.year - 1,
            self.fecha_seleccionada.month,
            1
        )
        self.actualizar_calendario()
    
    def next_year(self, instance):
        """Año siguiente"""
        self.fecha_seleccionada = datetime(
            self.fecha_seleccionada.year + 1,
            self.fecha_seleccionada.month,
            1
        )
        self.actualizar_calendario()


class CalculadoraTramosApp(App):
    """Aplicación principal"""
    
    def build(self):
        self.title = "Calculadora de Tramos"
        
        # Fechas seleccionadas
        self.fecha_inicial = None
        self.fecha_final = None
        
        # Valores económicos
        self.valor_tramo2 = 0
        self.valor_tramo3 = 0
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        
        # Título
        titulo = Label(
            text=f'Calculadora de\nTramos por Fechas',
            font_size='30sp',
            bold=True,
            size_hint_y=None,
            height=dp(50),
            color = (1, 0.6, 0.3, 1),
            halign="center",
            valign="middle"
        )
        layout.add_widget(titulo)
        
        # Indicaciones
        indicaciones = Label(
            text='Introduce las fechas.',
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(indicaciones)

        # Sección de fechas
        fechas_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            spacing=dp(10)
        )
        
        # Fecha inicial
        fecha_ini_layout = BoxLayout(size_hint_y=None, height=dp(39), spacing=dp(10))
            #Cuadro blanco fecha inicial
        self.input_fecha_inicial = TextInput(
            text='Fecha Inicial',
            font_size='21sp',
            readonly=True,
            size_hint_x=0.45, #Espacio del cuadro blanco
            multiline=False,
            background_color=(0.95, 0.95, 0.95, 1)
        )
        fecha_ini_layout.add_widget(self.input_fecha_inicial)
        
        btn_cal_inicial = Button(   #Btn calendario
            text='Calendario',
            size_hint_x=0.2,
            on_press=lambda x: self.abrir_calendario('inicial'),
            background_color=(0.3, 0.6, 1, 1)
        )
        fecha_ini_layout.add_widget(btn_cal_inicial)
        fechas_layout.add_widget(fecha_ini_layout)
        
        # Fecha final
        fecha_fin_layout = BoxLayout(size_hint_y=None, height=dp(39), spacing=dp(10))
            #Cuadro blanco fecha inicial
        self.input_fecha_final = TextInput(
            text='Fecha Final',
            font_size='21sp',
            readonly=True,
            size_hint_x=0.45,
            multiline=False,
            background_color=(0.95, 0.95, 0.95, 1)
        )
        fecha_fin_layout.add_widget(self.input_fecha_final)
        
        btn_cal_final = Button(
            text='Calendario',
            size_hint_x=0.2,
            on_press=lambda x: self.abrir_calendario('final'),
            background_color=(0.3, 0.6, 1, 1)
        )
        fecha_fin_layout.add_widget(btn_cal_final)
        
        fechas_layout.add_widget(fecha_fin_layout)
        
        layout.add_widget(fechas_layout)
        
        # Sección de valores económicos
        economicos_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            spacing=dp(10)
        )
        
        # Valor Tramo 2
        valor_t2_layout = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(10))
        valor_t2_layout.add_widget(Label(
            text='€/día Tramo 2:',
            size_hint_x=0.35,
            font_size='20sp'
        ))
        
        self.input_valor_t2 = TextInput(
            text='0',
            size_hint_x=0.45,
            font_size='19sp',
            multiline=False,
            input_filter='float',
            background_color=(0.95, 0.95, 0.95, 1)
        )
        valor_t2_layout.add_widget(self.input_valor_t2)
        economicos_layout.add_widget(valor_t2_layout)
        
        # Valor Tramo 3
        valor_t3_layout = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(10))
        valor_t3_layout.add_widget(Label(
            text='€/día Tramo 3:',
            size_hint_x=0.35,
            font_size='20sp'
        ))
        
        self.input_valor_t3 = TextInput(
            text='0',
            size_hint_x=0.45,
            font_size='19sp',
            multiline=False,
            input_filter='float',
            background_color=(0.95, 0.95, 0.95, 1)
        )
        valor_t3_layout.add_widget(self.input_valor_t3)
        economicos_layout.add_widget(valor_t3_layout)
        
        layout.add_widget(economicos_layout)
        
        # Botón calcular
        self.btn_calcular = Button(
            text='CALCULAR',
            size_hint_y=None,
            height=dp(60),
            font_size='25sp',
            bold=True,
            background_color=(0.3, 0.7, 0.3, 1),
            on_press=self.calcular_tramos
        )
        layout.add_widget(self.btn_calcular)
        
        # Separador
        layout.add_widget(Label(
            text='_' * 50,
            size_hint_y=None,
            height=dp(10)
        ))
        
        # Área de resultados con scroll
        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )

        self.resultados_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            padding=dp(5)
        )

        self.resultados_layout.bind(
            minimum_height=self.resultados_layout.setter('height')
        )

        scroll.add_widget(self.resultados_layout)
        layout.add_widget(scroll)
        
        return layout
    
    def abrir_calendario(self, tipo):
        """Abre el popup del calendario"""
        fecha_actual = self.fecha_inicial if tipo == 'inicial' and self.fecha_inicial else datetime.now()
        if tipo == 'final' and self.fecha_final:
            fecha_actual = self.fecha_final
        
        popup = CalendarioPopup(
            callback=lambda fecha: self.fecha_seleccionada(fecha, tipo),
            fecha_inicial=fecha_actual
        )
        popup.open()
    
    def fecha_seleccionada(self, fecha, tipo):
        """Callback cuando se selecciona una fecha"""
        fecha_formateada = fecha.strftime("%d/%m/%Y")
        
        if tipo == 'inicial':
            self.fecha_inicial = fecha
            self.input_fecha_inicial.text = fecha_formateada
        else:
            self.fecha_final = fecha
            self.input_fecha_final.text = fecha_formateada
    
    def mostrar_error(self, mensaje):
        """Muestra un popup de error"""
        contenido = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        contenido.add_widget(Label(text=mensaje, font_size='16sp'))
        
        btn_cerrar = Button(
            text='Aceptar',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.3, 0.6, 1, 1)
        )
        contenido.add_widget(btn_cerrar)
        
        popup = Popup(
            title='Error',
            content=contenido,
            size_hint=(0.8, 0.4)
        )
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()
    
    def calcular_tramos(self, instance):
        """Calcula los tres tramos según las especificaciones"""
        # Validar que se hayan seleccionado ambas fechas
        if not self.fecha_inicial:
            self.mostrar_error("Por favor, selecciona la fecha inicial.")
            return
        
        if not self.fecha_final:
            self.mostrar_error("Por favor, selecciona la fecha final.")
            return
        
        # Validar que la fecha final sea posterior
        if self.fecha_final <= self.fecha_inicial:
            self.mostrar_error("La fecha final debe ser posterior a la fecha inicial.")
            return
        
        # Obtener valores económicos
        try:
            self.valor_tramo2 = float(self.input_valor_t2.text) if self.input_valor_t2.text else 0
        except ValueError:
            self.valor_tramo2 = 0
        
        try:
            self.valor_tramo3 = float(self.input_valor_t3.text) if self.input_valor_t3.text else 0
        except ValueError:
            self.valor_tramo3 = 0
        
        # Limpiar resultados anteriores
        self.resultados_layout.clear_widgets()
        
        # Título de resultados
        self.resultados_layout.add_widget(Label(
            text='RESULTADOS',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(20),
            color=(0.2, 0.2, 0.2, 1)
        ))
        
        # Calcular días totales
        total_dias = (self.fecha_final - self.fecha_inicial).days + 1
        
        # TRAMO 1: 13 días naturales
        tramo1_inicio = self.fecha_inicial
        tramo1_dias = min(13, total_dias)  # Máximo 13 días o los que haya
        tramo1_fin = tramo1_inicio + timedelta(days=tramo1_dias - 1)
        
        self.mostrar_tramo(1, tramo1_inicio, tramo1_fin, tramo1_dias)
        
        # TRAMO 2: 7 días naturales (solo si hay más de 13 días)
        if total_dias > 13:
            tramo2_inicio = tramo1_fin + timedelta(days=1)
            dias_restantes = total_dias - 13
            tramo2_dias = min(7, dias_restantes)  # Máximo 7 días o los que queden
            tramo2_fin = tramo2_inicio + timedelta(days=tramo2_dias - 1)
            
            importe_t2 = tramo2_dias * self.valor_tramo2
            self.mostrar_tramo(2, tramo2_inicio, tramo2_fin, tramo2_dias, importe_t2)
        
        # TRAMO 3: Resto hasta fecha final (solo si hay más de 20 días)
        if total_dias > 20:
            tramo3_inicio = tramo1_fin + timedelta(days=8)  # 13 + 7 + 1
            tramo3_fin = self.fecha_final
            tramo3_dias = (tramo3_fin - tramo3_inicio).days + 1
            
            importe_t3 = tramo3_dias * self.valor_tramo3
            self.mostrar_tramo(3, tramo3_inicio, tramo3_fin, tramo3_dias, importe_t3)
        
        # Resumen total
        resumen = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            padding=dp(10),
            spacing=dp(5)
        )
        resumen.add_widget(Label(
            text=f'Total del período: {total_dias} días naturales',
            font_size='18sp',
            bold=True,
            color=(0.1, 0.4, 0.7, 1)
        ))
        
        # Calcular importe total
        importe_total = 0
        if total_dias > 13:
            dias_t2 = min(7, total_dias - 13)
            importe_total += dias_t2 * self.valor_tramo2
        if total_dias > 20:
            dias_t3 = total_dias - 20
            importe_total += dias_t3 * self.valor_tramo3
        
        if importe_total > 0:
            resumen.add_widget(Label(
                text=f'Importe total: {importe_total:.2f} €',
                font_size='22sp',
                bold=True,
                color=(0.1, 0.7, 0.1, 1)
            ))
        
        self.resultados_layout.add_widget(resumen)
    
    def mostrar_tramo(self, numero, fecha_inicio, fecha_fin, dias, importe=None):
        tramo_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(10),
            spacing=dp(5)
        )
        tramo_layout.bind(minimum_height=tramo_layout.setter('height'))

        tramo_layout.add_widget(Label(
            text=f'TRAMO {numero}',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=(0.13, 0.59, 0.95, 1)
        ))

        info_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        info_layout.bind(minimum_height=info_layout.setter('height'))

        info_layout.add_widget(Label(
            text=f'Fecha de inicio: {fecha_inicio.strftime("%d/%m/%Y")}',
            font_size='18sp',
            size_hint_y=None,
            height=dp(25)
        ))

        info_layout.add_widget(Label(
            text=f'Número de días: {dias} días.',
            font_size='18sp',
            size_hint_y=None,
            height=dp(25),
            bold=True
        ))

        info_layout.add_widget(Label(
            text=f'Fecha de fin: {fecha_fin.strftime("%d/%m/%Y")}',
            font_size='18sp',
            size_hint_y=None,
            height=dp(25),
            bold=True,
            color=(1, 0.6, 0.3, 1)
        ))

        if importe is not None and importe > 0:
            info_layout.add_widget(Label(
                text=f'Importe: {importe:.2f} €',
                font_size='18sp',
                size_hint_y=None,
                height=dp(25),
                bold=True,
                color=(0.1, 0.6, 0.1, 1)
            ))

        tramo_layout.add_widget(info_layout)
        self.resultados_layout.add_widget(tramo_layout)

        self.resultados_layout.add_widget(Label(
            text='=' * 40,
            size_hint_y=None,
            height=dp(20)
        ))



if __name__ == '__main__':
    CalculadoraTramosApp().run()
