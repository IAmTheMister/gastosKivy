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
import csv
import json
from functools import partial
from datetime import datetime

categorias = ["Gasolina", "Hogar", "Transporte", "Dulces", "Ocio",
              "Caprichos", "Comida", "Restaurantes", "Medicamentos",
              "Alquiler", "Viajes"]

class Intervalo:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.22

    def menu_intervalo(self,usuario):
        self.layout_intervalo = GridLayout(cols=1, spacing=10)
        self.layout_stats_intervalo = GridLayout(cols=1, size_hint_y=None)
        self.layout_navegacion_intervalo = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_inputs_intervalo = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_botones_intervalo = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)
        
        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_intervalo), height=Window.height * 0.05,
                            size_hint_y=None, background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_intervalo.add_widget(btn_exit)
        self.layout_navegacion_intervalo.add_widget(btn_volver)
        self.layout_intervalo.add_widget(self.layout_navegacion_intervalo)

        self.input_inicio = TextInput(hint_text='Inicio intervalo (dd/mm/yyyy)', multiline=False,
                                      height=Window.height * 0.05, size_hint_y=None)
        self.input_fin = TextInput(hint_text='Fin intervalo (dd/mm/yyyy)', multiline=False, height=Window.height * 0.05,
                                   size_hint_y=None)
        
        self.layout_inputs_intervalo.add_widget(self.input_inicio)
        self.layout_inputs_intervalo.add_widget(self.input_fin)
        self.layout_intervalo.add_widget(self.layout_inputs_intervalo)

        btn_mostrar_stats = Button(text='Estadísticas', on_press=partial(self.stats_intervalo,usuario),
                                   height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_categoria = Button(text='Categoria', on_press=partial(self.categoria_intervalo,usuario),
                                       height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_gastos = Button(text='Gastos', on_press=partial(self.gastos_intervalo,usuario),
                                    height=Window.height * 0.05, size_hint_y=None)

        self.layout_botones_intervalo.add_widget(btn_mostrar_stats)
        self.layout_botones_intervalo.add_widget(btn_mostrar_categoria)
        self.layout_botones_intervalo.add_widget(btn_mostrar_gastos)
        self.layout_intervalo.add_widget(self.layout_botones_intervalo)

    
        self.layout_intervalo.add_widget(self.layout_stats_intervalo)
        self.main_layout.add_widget(self.layout_intervalo)

    def stats_intervalo(self,usuario, instance):
        if len(self.layout_stats_intervalo.children) > 0:
            self.layout_stats_intervalo.clear_widgets()
            self.altura = 0.22
        else:
            self.calcular_stats_intervalo(usuario)

    def categoria_intervalo(self,usuario, instance):
        if len(self.layout_stats_intervalo.children) > 0:
            self.layout_stats_intervalo.clear_widgets()
            self.altura = 0.22
        else:
            self.calcular_gasto_categorias_intervalo(usuario)

    def gastos_intervalo(self,usuario, instance):
        if len(self.layout_stats_intervalo.children) > 0:
            self.layout_stats_intervalo.clear_widgets()
            self.altura = 0.22
        else:
            self.mostrar_lista_gastos_intervalo(usuario)

    def calcular_stats_intervalo(self, usuario):
        inicio = self.input_inicio.text
        fin = self.input_fin.text
        gasto_total, ingresos = self.calcular_saldo_intervalo(fin, inicio, usuario)
        self.layout_saldo_intervalo = GridLayout(cols=2, height=Window.height * 0.15,
                                                 size_hint_y=None)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_total,2))+" €", height=Window.height * 0.05, size_hint_y=None)

        nombre_ingreso = Label(text="Ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_ingreso = Label(text=str(round(ingresos, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_saldo = Label(text="Saldo:", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo = Label(text=str(round(ingresos - gasto_total, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        self.layout_saldo_intervalo.add_widget(nombre_ingreso)
        self.layout_saldo_intervalo.add_widget(valor_ingreso)

        self.layout_saldo_intervalo.add_widget(nombre_gasto)
        self.layout_saldo_intervalo.add_widget(valor_gasto)

        self.layout_saldo_intervalo.add_widget(nombre_saldo)
        self.layout_saldo_intervalo.add_widget(valor_saldo)

        self.layout_stats_intervalo.add_widget(self.layout_saldo_intervalo)
        self.altura += 0.15

    def calcular_saldo_intervalo(self, fin, inicio, usuario):
        gasto_total = 0
        ingresos = 0
        with open(usuario + "/ingresos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
                fecha_fin = datetime.strptime(fin, "%d/%m/%Y")
                if row and fecha_inicio <= fecha_row <= fecha_fin:
                    ingresos += round(float(row[1]), 2)
        with open(usuario + "/gastos" + "_" + usuario + ".csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
                fecha_fin = datetime.strptime(fin, "%d/%m/%Y")
                if row and fecha_inicio <= fecha_row <= fecha_fin:
                    gasto_total += round(float(row[3]), 2)
        return gasto_total, ingresos

    def calcular_gasto_categorias_intervalo(self,usuario):
        inicio = self.input_inicio.text
        fin = self.input_fin.text

        self.layout_encabezados_categoria_intervalo = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)
        encabezado_categoria = Label(text="Categoría", height=Window.height * 0.05, size_hint_y=None)
        encabezado_gasto = Label(text="Gasto", height=Window.height * 0.05, size_hint_y=None)
        encabezado_porcentaje = Label(text="%", height=Window.height * 0.05, size_hint_y=None)
        self.layout_encabezados_categoria_intervalo.add_widget(encabezado_categoria)
        self.layout_encabezados_categoria_intervalo.add_widget(encabezado_gasto)
        self.layout_encabezados_categoria_intervalo.add_widget(encabezado_porcentaje)
        self.layout_stats_intervalo.add_widget(self.layout_encabezados_categoria_intervalo)

        gasto_intervalo, ingresos_intervalo = self.calcular_saldo_intervalo(fin, inicio, usuario)
        
        for i in range(len(categorias)):
            self.layout_categoria_intervalo = GridLayout(cols=3, rows=1, height=Window.height * 0.05,
                                               size_hint_y=None)
            gasto_categoría = 0
            with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                    fecha_inicio = datetime.strptime(self.input_inicio.text, "%d/%m/%Y")
                    fecha_fin = datetime.strptime(self.input_fin.text, "%d/%m/%Y")
                    if row and row[2] == categorias[i] and fecha_row >= fecha_inicio and fecha_row <= fecha_fin:
                        gasto_categoría += round(float(row[3]), 2)
            if gasto_categoría > 0:
                nombre = Label(text=categorias[i], height=Window.height * 0.05, size_hint_y=None)
                valor = Label(text=str(round(gasto_categoría,2))+" €", height=Window.height * 0.05, size_hint_y=None)
                porcentaje = Label(text=str(round(gasto_categoría / gasto_intervalo * 100, 2)) + "%",
                                   height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_intervalo.add_widget(nombre)
                self.layout_categoria_intervalo.add_widget(valor)
                self.layout_categoria_intervalo.add_widget(porcentaje)
                self.layout_stats_intervalo.add_widget(self.layout_categoria_intervalo)
                self.altura += 0.05

    def mostrar_lista_gastos_intervalo(self,usuario):
        self.scrollview_intervalo = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)

        self.layout_gasto_intervalo = GridLayout(cols=4, size_hint_y=None)
        self.layout_gasto_intervalo.bind(minimum_height=self.layout_gasto_intervalo.setter('height'))

        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                fecha_inicio = datetime.strptime(self.input_inicio.text, "%d/%m/%Y")
                fecha_fin = datetime.strptime(self.input_fin.text, "%d/%m/%Y")
                if row and fecha_inicio <= fecha_row <= fecha_fin:
                    self.label_fecha_intervalo = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                    self.label_concepto_intervalo = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                    self.label_categoria_intervalo = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                    self.label_precio_intervalo = Label(text=row[3]+" €", height=Window.height * 0.05, size_hint_y=None)

                    self.layout_gasto_intervalo.add_widget(self.label_fecha_intervalo)
                    self.layout_gasto_intervalo.add_widget(self.label_concepto_intervalo)
                    self.layout_gasto_intervalo.add_widget(self.label_categoria_intervalo)
                    self.layout_gasto_intervalo.add_widget(self.label_precio_intervalo)

        self.scrollview_intervalo.add_widget(self.layout_gasto_intervalo)
        self.layout_stats_intervalo.add_widget(self.scrollview_intervalo)

    def boton_volver_intervalo(self, instance):
        self.main_layout.remove_widget(self.layout_intervalo)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()