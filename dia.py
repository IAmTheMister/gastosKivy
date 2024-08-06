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

class Dia:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.22

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
            self.gasto_dia(usuario)

    def boton_categoria_dia(self, usuario, instance):
        if len(self.layout_stats_dia.children) > 0:
            self.layout_stats_dia.clear_widgets()
        else:
            self.calcular_gasto_categorias_dia(usuario)

    def boton_gastos_dia(self, usuario, instance):
        if len(self.layout_stats_dia.children) > 0:
            self.layout_stats_dia.clear_widgets()
        else:
            self.mostrar_lista_gastos_dia(usuario)

    def mostrar_lista_gastos_dia(self,usuario):
        self.scrollview_dia = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)
        self.layout_gasto_dia = GridLayout(cols=4, size_hint_y=None)
        self.layout_gasto_dia.bind(minimum_height=self.layout_gasto_dia.setter('height'))

        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row and row[0] == self.input_dia.text:
                    self.label_fecha = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                    self.label_concepto = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                    self.label_categoria = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                    self.label_precio = Label(text=row[3]+" €", height=Window.height * 0.05, size_hint_y=None)

                    self.layout_gasto_dia.add_widget(self.label_fecha)
                    self.layout_gasto_dia.add_widget(self.label_concepto)
                    self.layout_gasto_dia.add_widget(self.label_categoria)
                    self.layout_gasto_dia.add_widget(self.label_precio)

        self.scrollview_dia.add_widget(self.layout_gasto_dia)
        self.layout_stats_dia.add_widget(self.scrollview_dia)

    def calcular_gasto_categorias_dia(self,usuario):
        gasto_dia = self.calcular_gasto_dia(usuario, self.input_dia.text)
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
                valor = Label(text=str(round(gasto_categoría,2))+" €", height=Window.height * 0.05, size_hint_y=None)
                porcentaje = Label(text=str(round(gasto_categoría/gasto_dia*100, 2)) + "%", height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria.add_widget(nombre)
                self.layout_categoria.add_widget(valor)
                self.layout_categoria.add_widget(porcentaje)
                self.layout_stats_dia.add_widget(self.layout_categoria)

    def gasto_dia(self, usuario):
        gasto_total = self.calcular_gasto_dia(usuario, self.input_dia.text)
        self.layout_gasto_total = GridLayout(cols=2, rows=1, height=Window.height * 0.05,
                                             size_hint_y=None)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_total,2))+" €", height=Window.height * 0.05, size_hint_y=None)
        self.layout_gasto_total.add_widget(nombre_gasto)
        self.layout_gasto_total.add_widget(valor_gasto)
        self.layout_stats_dia.add_widget(self.layout_gasto_total)

    def calcular_gasto_dia(self, usuario, dia):
        gasto_total = 0
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row and row[0] == dia:
                    gasto_total += round(float(row[3]), 2)
        return gasto_total

    def boton_volver_dia(self, instance):
        self.main_layout.remove_widget(self.layout_dia)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()