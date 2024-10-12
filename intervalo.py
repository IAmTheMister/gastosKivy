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
              "Alquiler", "Viajes"]


class Intervalo:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.27

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
        else:
            self.mostrar_stats_intervalo(usuario)

    def categoria_intervalo(self,usuario, instance):
        if len(self.layout_stats_intervalo.children) > 0:
            self.layout_stats_intervalo.clear_widgets()
        else:
            self.mostrar_gasto_categorias_intervalo(usuario)

    def gastos_intervalo(self,usuario, instance):
        if len(self.layout_stats_intervalo.children) > 0:
            self.layout_stats_intervalo.clear_widgets()
        else:
            self.mostrar_gastos_intervalo(usuario)

    def mostrar_stats_intervalo(self, usuario):
        clase_calc = Calculos()
        inicio = self.input_inicio.text
        fin = self.input_fin.text
        gasto_total, ingresos = clase_calc.calcular_saldo_intervalo(fin, inicio, usuario)
        gasto_ing = clase_calc.calcular_gasto_ing_intervalo(fin, inicio, usuario)
        gasto_ahorros = clase_calc.calcular_gasto_ahorros_intervalo(fin, inicio, usuario)
        self.layout_saldo_intervalo = GridLayout(cols=2, height=Window.height * 0.15,
                                                 size_hint_y=None)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_total,2))+" €", height=Window.height * 0.05, size_hint_y=None)

        nombre_ingreso = Label(text="Ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_ingreso = Label(text=str(round(ingresos, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_saldo = Label(text="Saldo (total):", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo = Label(text=str(round(ingresos - gasto_total, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_saldo_ing = Label(text="Saldo (ingresos):", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo_ing = Label(text=str(round(ingresos - gasto_ing, 2)) + " €", height=Window.height * 0.05,
                                size_hint_y=None)

        nombre_gasto_ing = Label(text="Gastos financiados con ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto_ing = Label(text=str(round(gasto_ing, 2)) + " €", height=Window.height * 0.05,
                            size_hint_y=None)

        nombre_gasto_ahorros = Label(text="Gastos financiados con ahorros:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto_ahorros = Label(text=str(round(gasto_ahorros, 2)) + " €", height=Window.height * 0.05,
                            size_hint_y=None)

        self.layout_saldo_intervalo.add_widget(nombre_ingreso)
        self.layout_saldo_intervalo.add_widget(valor_ingreso)

        self.layout_saldo_intervalo.add_widget(nombre_gasto)
        self.layout_saldo_intervalo.add_widget(valor_gasto)

        self.layout_saldo_intervalo.add_widget(nombre_saldo)
        self.layout_saldo_intervalo.add_widget(valor_saldo)

        self.layout_saldo_intervalo.add_widget(nombre_saldo_ing)
        self.layout_saldo_intervalo.add_widget(valor_saldo_ing)

        self.layout_saldo_intervalo.add_widget(nombre_gasto_ing)
        self.layout_saldo_intervalo.add_widget(valor_gasto_ing)

        self.layout_saldo_intervalo.add_widget(nombre_gasto_ahorros)
        self.layout_saldo_intervalo.add_widget(valor_gasto_ahorros)

        self.layout_stats_intervalo.add_widget(self.layout_saldo_intervalo)

    def mostrar_gasto_categorias_intervalo(self, usuario):
        clase_calc = Calculos()

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

        gasto_intervalo, ingresos_intervalo = clase_calc.calcular_saldo_intervalo(fin, inicio, usuario)
        
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

    def mostrar_gastos_intervalo(self, usuario):
        self.layout_gastos_intervalo = GridLayout(cols=1)
        self.layout_botones_buscar_intervalo = GridLayout(cols=2, size_hint_y=None, height=Window.height * 0.05)
        self.scrollview_intervalo = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)
        self.layout_lista_gastos_intervalo = GridLayout(cols=5, size_hint_y=None)
        self.layout_lista_gastos_intervalo.bind(minimum_height=self.layout_lista_gastos_intervalo.setter('height'))
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
        self.layout_botones_buscar_intervalo.add_widget(self.mainbutton_categoria)

        btn_buscar = Button(text="Buscar", on_press=partial(self.buscar_gastos_intervalo, usuario),
                            size_hint_y=None, height=Window.height * 0.05)
        self.layout_botones_buscar_intervalo.add_widget(btn_buscar)
        self.layout_gastos_intervalo.add_widget(self.layout_botones_buscar_intervalo)
        self.layout_stats_intervalo.add_widget(self.layout_gastos_intervalo)

    def buscar_gastos_intervalo(self, usuario, instance):
        if len(self.layout_lista_gastos_intervalo.children) > 0:
            self.layout_gastos_intervalo.remove_widget(self.scrollview_intervalo)
            self.scrollview_intervalo.remove_widget(self.layout_lista_gastos_intervalo)
            self.layout_lista_gastos_intervalo.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_lista_gastos_intervalo(usuario)

    def mostrar_lista_gastos_intervalo(self, usuario):
        fecha_inicio = datetime.strptime(self.input_inicio.text, "%d/%m/%Y")
        fecha_fin = datetime.strptime(self.input_fin.text, "%d/%m/%Y")
        cat = self.mainbutton_categoria.text
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if cat == "Categoria":
                    if row and fecha_inicio <= fecha_row <= fecha_fin:
                        label_fecha_intervalo = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_intervalo = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_intervalo = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_intervalo = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_intervalo = Label(text=row[4], height=Window.height * 0.05,
                                                       size_hint_y=None)

                        self.layout_lista_gastos_intervalo.add_widget(label_fecha_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_concepto_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_categoria_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_precio_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_fuente_intervalo)
                else:
                    if row and fecha_inicio <= fecha_row <= fecha_fin and row[2] == cat:
                        label_fecha_intervalo = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_intervalo = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_intervalo = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_intervalo = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_intervalo = Label(text=row[4], height=Window.height * 0.05,
                                                       size_hint_y=None)

                        self.layout_lista_gastos_intervalo.add_widget(label_fecha_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_concepto_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_categoria_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_precio_intervalo)
                        self.layout_lista_gastos_intervalo.add_widget(label_fuente_intervalo)

        if len(self.layout_lista_gastos_intervalo.children) == 0:
            label_no_gastos = Label(text="No hay gastos", height=Window.height * 0.05, size_hint_y=None)
            self.layout_lista_gastos_intervalo.add_widget(label_no_gastos)

        self.scrollview_intervalo.add_widget(self.layout_lista_gastos_intervalo)
        self.layout_gastos_intervalo.add_widget(self.scrollview_intervalo)

    def boton_volver_intervalo(self, instance):
        self.main_layout.remove_widget(self.layout_intervalo)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()