"""
Calculadora de Tramos v1.0 Beta
Creado por Luca - Producido por Nebula Studios

Estructura modular:
- config/colores.py: Colores de la interfaz
- config/tamano.py: Tamaños y espaciados
- textos/es.py: Textos en español
- app/calculadora.py: UI principal
- main.py: Punto de entrada
"""

from kivy.app import App
from app.calculadora import CalculadoraLayout


class CalculadoraTramosApp(App):
    """Aplicación principal de Kivy"""
    
    def build(self):
        """Construye y devuelve el widget raíz"""
        self.title = "Calculadora de Tramos v1.0"
        return CalculadoraLayout()


if __name__ == '__main__':
    app = CalculadoraTramosApp()
    app.run()
