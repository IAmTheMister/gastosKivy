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

categorias = ["Gasolina", "Hogar", "Transporte", "Dulces", "Ocio",
              "Caprichos", "Comida", "Restaurantes", "Medicamentos",
              "Alquiler", "Viajes"]


class Ano:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.22

    def menu_ano(self, usuario):
        self.layout_ano = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_stats_ano = GridLayout(cols=1)

        self.layout_navegacion_ano = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_botones_ano = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_ano), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_ano.add_widget(btn_exit)
        self.layout_navegacion_ano.add_widget(btn_volver)
        self.layout_ano.add_widget(self.layout_navegacion_ano)

        self.input_ano = TextInput(hint_text='Año (yyyy)', multiline=False,
                                   height=Window.height * 0.05, size_hint_y=None)

        self.layout_ano.add_widget(self.input_ano)

        btn_mostrar_stats = Button(text='Estadísticas', on_press=partial(self.stats_ano,usuario),
                                   height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_categoria = Button(text='Categoria', on_press=partial(self.categoria_ano,usuario),
                                       height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_gastos = Button(text='Gastos', on_press = partial(self.gastos_ano,usuario),
                                       height=Window.height * 0.05, size_hint_y=None)

        self.layout_botones_ano.add_widget(btn_mostrar_stats)
        self.layout_botones_ano.add_widget(btn_mostrar_categoria)
        self.layout_botones_ano.add_widget(btn_mostrar_gastos)
        self.layout_ano.add_widget(self.layout_botones_ano)

        self.layout_ano.add_widget(self.layout_stats_ano)
        self.main_layout.add_widget(self.layout_ano)

    def stats_ano(self,usuario, instance):
        if len(self.layout_stats_ano.children) > 0:
            self.layout_stats_ano.clear_widgets()
        else:
            self.calcular_saldo_ano(usuario)

    def categoria_ano(self,usuario, instance):
        if len(self.layout_stats_ano.children) > 0:
            self.layout_stats_ano.clear_widgets()
        else:
            self.calcular_gasto_categorias_ano(usuario)

    def gastos_ano(self,usuario, instance):
        if len(self.layout_stats_ano.children) > 0:
            self.layout_stats_ano.clear_widgets()
        else:
            self.mostrar_lista_gastos_ano(usuario)

    def calcular_saldo_ano(self,usuario):
        gasto_total = 0
        ingresos = 0

        with open(usuario + "/ingresos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                ano = int(self.input_ano.text)
                if row and fecha_row.year == ano:
                    ingresos += round(float(row[1]), 2)

        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                ano = int(self.input_ano.text)
                if row and fecha_row.year == ano:
                    gasto_total += round(float(row[3]), 2)
        self.layout_saldo_ano = GridLayout(cols=2, height=Window.height * 0.15,
                                           size_hint_y=None)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_total, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_ingreso = Label(text="Ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_ingreso = Label(text=str(round(ingresos, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_saldo = Label(text="Saldo:", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo = Label(text=str(round(ingresos - gasto_total, 2)) + " €", height=Window.height * 0.05,
                            size_hint_y=None)

        self.layout_saldo_ano.add_widget(nombre_ingreso)
        self.layout_saldo_ano.add_widget(valor_ingreso)

        self.layout_saldo_ano.add_widget(nombre_gasto)
        self.layout_saldo_ano.add_widget(valor_gasto)

        self.layout_saldo_ano.add_widget(nombre_saldo)
        self.layout_saldo_ano.add_widget(valor_saldo)

        self.layout_stats_ano.add_widget(self.layout_saldo_ano)

    def calcular_gasto_categorias_ano(self,usuario):
        for i in range(len(categorias)):
            self.layout_categoria_ano = GridLayout(cols=2, rows=1, height=Window.height * 0.05,
                                                   size_hint_y=None)
            gasto_categoría = 0
            with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                    ano = int(self.input_ano.text)
                    if row and row[2] == categorias[i] and fecha_row.year == ano:
                        gasto_categoría += round(float(row[3]), 2)
            if gasto_categoría > 0:
                nombre = Label(text=categorias[i], height=Window.height * 0.05, size_hint_y=None)
                valor = Label(text=str(round(gasto_categoría, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_ano.add_widget(nombre)
                self.layout_categoria_ano.add_widget(valor)
                self.layout_stats_ano.add_widget(self.layout_categoria_ano)

    def mostrar_lista_gastos_ano(self,usuario):
        self.scrollview_ano = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)

        self.layout_gasto_ano = GridLayout(cols=4, size_hint_y=None)
        self.layout_gasto_ano.bind(minimum_height=self.layout_gasto_ano.setter('height'))

        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                ano = int(self.input_ano.text)
                if row and fecha_row.year == ano:
                    label_fecha_ano = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                    label_concepto_ano = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                    label_categoria_ano = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                    label_precio_ano = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)

                    self.layout_gasto_ano.add_widget(label_fecha_ano)
                    self.layout_gasto_ano.add_widget(label_concepto_ano)
                    self.layout_gasto_ano.add_widget(label_categoria_ano)
                    self.layout_gasto_ano.add_widget(label_precio_ano)

        self.scrollview_ano.add_widget(self.layout_gasto_ano)
        self.layout_stats_ano.add_widget(self.scrollview_ano)

    def boton_volver_ano(self, instance):
        self.main_layout.remove_widget(self.layout_ano)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()