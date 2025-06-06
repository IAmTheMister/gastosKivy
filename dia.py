from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
import csv
import json
from functools import partial
from datetime import datetime

from calculos import Calculos

categorias = ["Gasolina", "Hogar", "Transporte", "Dulces", "Ocio",
              "Caprichos", "Comida", "Restaurantes", "Medicamentos",
              "Alquiler", "Viajes", "Coche", "Merienda"]

class Dia:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.27

    def menu_dia(self,usuario):
        self.layout_dia = GridLayout(cols=1, spacing=10)
        self.layout_stats_dia = GridLayout(cols=1, size_hint_y=None)

        self.layout_navegacion_dia = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_botones_dia = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                               background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))
        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_dia), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_dia.add_widget(btn_exit)
        self.layout_navegacion_dia.add_widget(btn_volver)
        self.layout_dia.add_widget(self.layout_navegacion_dia)

        self.input_dia = TextInput(hint_text='Elige Dia (dd/mm/yyyy)', multiline=False, height=Window.height * 0.05,
                                   size_hint_y=None)
        
        self.layout_dia.add_widget(self.input_dia)

        btn_mostrar_stats = Button(text='Estadísticas', on_press=partial(self.boton_stats_dia, usuario),
                                   height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_categoria = Button(text='Categoria', on_press=partial(self.boton_categoria_dia, usuario),
                                       height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_gastos = Button(text='Gastos', on_press=partial(self.boton_gastos_dia, usuario),
                                    height=Window.height * 0.05, size_hint_y=None)

        self.layout_botones_dia.add_widget(btn_mostrar_stats)
        self.layout_botones_dia.add_widget(btn_mostrar_categoria)
        self.layout_botones_dia.add_widget(btn_mostrar_gastos)
        self.layout_dia.add_widget(self.layout_botones_dia)

        self.layout_dia.add_widget(self.layout_stats_dia)
        self.main_layout.add_widget(self.layout_dia)

    def boton_stats_dia(self, usuario, instance):
        if len(self.layout_stats_dia.children) > 0:
            self.layout_stats_dia.clear_widgets()
        else:
            self.mostrar_stats_dia(usuario)

    def boton_categoria_dia(self, usuario, instance):
        if len(self.layout_stats_dia.children) > 0:
            self.layout_stats_dia.clear_widgets()
        else:
            self.mostrar_gasto_categorias_dia(usuario)

    def boton_gastos_dia(self, usuario, instance):
        if len(self.layout_stats_dia.children) > 0:
            self.layout_stats_dia.clear_widgets()
        else:
            self.mostrar_gastos_dia(usuario)

    def mostrar_gasto_categorias_dia(self, usuario):
        clase_calc = Calculos()
        gasto_dia = clase_calc.calcular_gasto_dia(usuario, self.input_dia.text)
        self.layout_encabezados_categoria_dia = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)
        encabezado_categoria = Label(text="Categoría", height=Window.height * 0.05, size_hint_y=None)
        encabezado_gasto = Label(text="Gasto", height=Window.height * 0.05, size_hint_y=None)
        encabezado_porcentaje = Label(text="%", height=Window.height * 0.05, size_hint_y=None)
        self.layout_encabezados_categoria_dia.add_widget(encabezado_categoria)
        self.layout_encabezados_categoria_dia.add_widget(encabezado_gasto)
        self.layout_encabezados_categoria_dia.add_widget(encabezado_porcentaje)
        self.layout_stats_dia.add_widget(self.layout_encabezados_categoria_dia)
        
        for i in range(len(categorias)):
            self.layout_categoria = GridLayout(cols=3, rows=1, height=Window.height * 0.05,
                                               size_hint_y=None)
            gasto_categoría = 0
            with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if row and row[2] == categorias[i] and row[0] == self.input_dia.text:
                        gasto_categoría += round(float(row[3]), 2)
            if gasto_categoría > 0:
                nombre = Label(text=categorias[i], height=Window.height * 0.05, size_hint_y=None)
                valor = Label(text=str(round(gasto_categoría,2))+" лв*", height=Window.height * 0.05, size_hint_y=None)
                porcentaje = Label(text=str(round(gasto_categoría/gasto_dia*100, 2)) + "%", height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria.add_widget(nombre)
                self.layout_categoria.add_widget(valor)
                self.layout_categoria.add_widget(porcentaje)
                self.layout_stats_dia.add_widget(self.layout_categoria)

    def mostrar_stats_dia(self, usuario):
        clase_calc = Calculos()
        gasto_total_dia = clase_calc.calcular_gasto_dia(usuario, self.input_dia.text)
        gasto_ing = clase_calc.calcular_gasto_ing_dia(usuario, self.input_dia.text)
        gasto_ahorros = clase_calc.calcular_gasto_ahorros_dia(usuario, self.input_dia.text)
        fecha_dia = datetime.strptime(self.input_dia.text, "%d/%m/%Y")
        gasto_total_mes, ingresos_mes = clase_calc.calcular_saldo_mes(usuario,fecha_dia.year, fecha_dia.month)
        alquiler_mes = clase_calc.calcular_alquiler_mes(usuario,fecha_dia.year, fecha_dia.month)
        self.layout_gasto_total = GridLayout(cols=2)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_total_dia,2))+" лв*", height=Window.height * 0.05, size_hint_y=None)
        self.layout_gasto_total.add_widget(nombre_gasto)
        self.layout_gasto_total.add_widget(valor_gasto)

        nombre_porcentaje = Label(text="% gasto mensual:", height=Window.height * 0.05, size_hint_y=None)
        valor_porcentaje = Label(text=str(round(gasto_total_dia/gasto_total_mes*100, 2)) + "%", height=Window.height * 0.05, size_hint_y=None)
        self.layout_gasto_total.add_widget(nombre_porcentaje)
        self.layout_gasto_total.add_widget(valor_porcentaje)

        nombre_porcentaje_sin = Label(text="% gasto mensual sin alquiler:", height=Window.height * 0.05, size_hint_y=None)
        valor_porcentaje_sin = Label(text=str(round(gasto_total_dia / (gasto_total_mes - alquiler_mes) * 100, 2)) + "%",
                                 height=Window.height * 0.05, size_hint_y=None)
        self.layout_gasto_total.add_widget(nombre_porcentaje_sin)
        self.layout_gasto_total.add_widget(valor_porcentaje_sin)

        nombre_gasto_ing = Label(text="Gasto procedente de ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto_ing = Label(text=str(round(gasto_ing, 2)) + " лв*", height=Window.height * 0.05,
                                size_hint_y=None)
        self.layout_gasto_total.add_widget(nombre_gasto_ing)
        self.layout_gasto_total.add_widget(valor_gasto_ing)

        nombre_gasto_ahorros = Label(text="Gasto procedente de ahorros:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto_ahorros = Label(text=str(round(gasto_ahorros, 2)) + " лв*", height=Window.height * 0.05,
                                    size_hint_y=None)
        self.layout_gasto_total.add_widget(nombre_gasto_ahorros)
        self.layout_gasto_total.add_widget(valor_gasto_ahorros)

        self.layout_stats_dia.add_widget(self.layout_gasto_total)

    def mostrar_gastos_dia(self, usuario):
        self.layout_gastos_dia = GridLayout(cols=1)
        self.layout_botones_buscar_dia = GridLayout(cols=2, size_hint_y=None, height=Window.height * 0.05)
        self.scrollview_dia = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)
        self.layout_lista_gastos_dia = GridLayout(cols=5, size_hint_y=None)
        self.layout_lista_gastos_dia.bind(minimum_height=self.layout_lista_gastos_dia.setter('height'))
        self.dropdown_categoria = DropDown()
        for cat in categorias:
            btn = Button(text=cat, size_hint_y=None, height=Window.height * 0.05)
            btn.bind(on_release=lambda btn: self.dropdown_categoria.select(btn.text))
            self.dropdown_categoria.add_widget(btn)

        btn_todas = Button(text="Categoria", size_hint_y=None, height=Window.height * 0.05)
        btn_todas.bind(on_release=lambda btn_todas: self.dropdown_categoria.select(btn_todas.text))
        self.dropdown_categoria.add_widget(btn_todas)

        self.mainbutton_categoria = Button(text='Categoria', height=Window.height * 0.05, size_hint_y=None)
        self.mainbutton_categoria.bind(on_release=self.dropdown_categoria.open)
        self.dropdown_categoria.bind(on_select=lambda instance, x: setattr(self.mainbutton_categoria, 'text', x))
        self.layout_botones_buscar_dia.add_widget(self.mainbutton_categoria)

        btn_buscar = Button(text="Buscar", on_press=partial(self.buscar_gastos_dia, usuario),
                            size_hint_y=None, height=Window.height * 0.05)
        self.layout_botones_buscar_dia.add_widget(btn_buscar)
        self.layout_gastos_dia.add_widget(self.layout_botones_buscar_dia)
        self.layout_stats_dia.add_widget(self.layout_gastos_dia)

    def buscar_gastos_dia(self, usuario, instance):
        if len(self.layout_lista_gastos_dia.children) > 0:
            self.layout_gastos_dia.remove_widget(self.scrollview_dia)
            self.scrollview_dia.remove_widget(self.layout_lista_gastos_dia)
            self.layout_lista_gastos_dia.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_lista_gastos_dia(usuario)

    def mostrar_lista_gastos_dia(self, usuario):
        cat = self.mainbutton_categoria.text
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if cat == "Categoria":
                    if row and row[0] == row[0] == self.input_dia.text:
                        label_fecha_dia = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_dia = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_dia = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_dia = Label(text=row[3] + " лв*", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_dia = Label(text=row[4], height=Window.height * 0.05, size_hint_y=None)

                        self.layout_lista_gastos_dia.add_widget(label_fecha_dia)
                        self.layout_lista_gastos_dia.add_widget(label_concepto_dia)
                        self.layout_lista_gastos_dia.add_widget(label_categoria_dia)
                        self.layout_lista_gastos_dia.add_widget(label_precio_dia)
                        self.layout_lista_gastos_dia.add_widget(label_fuente_dia)
                else:
                    if row and row[0] == self.input_dia.text and row[2] == cat:
                        label_fecha_dia = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_dia = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_dia = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_dia = Label(text=row[3] + " лв*", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_dia = Label(text=row[4], height=Window.height * 0.05, size_hint_y=None)

                        self.layout_lista_gastos_dia.add_widget(label_fecha_dia)
                        self.layout_lista_gastos_dia.add_widget(label_concepto_dia)
                        self.layout_lista_gastos_dia.add_widget(label_categoria_dia)
                        self.layout_lista_gastos_dia.add_widget(label_precio_dia)
                        self.layout_lista_gastos_dia.add_widget(label_fuente_dia)

        if len(self.layout_lista_gastos_dia.children) == 0:
            label_no_gastos = Label(text="No hay gastos", height=Window.height * 0.05, size_hint_y=None)
            self.layout_lista_gastos_dia.add_widget(label_no_gastos)

        self.scrollview_dia.add_widget(self.layout_lista_gastos_dia)
        self.layout_gastos_dia.add_widget(self.scrollview_dia)

    def boton_volver_dia(self, instance):
        self.main_layout.remove_widget(self.layout_dia)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()