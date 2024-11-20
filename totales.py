# -*- coding: utf-8 -*-
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
              "Alquiler", "Viajes", "Coche"]

class ClaseTotal:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.21

    def menu_total(self, usuario):
        self.layout_total = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_stats_total = GridLayout(cols=1)
        self.layout_navegacion_total = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_botones_total = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)
        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_total), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_total.add_widget(btn_exit)
        self.layout_navegacion_total.add_widget(btn_volver)
        self.layout_total.add_widget(self.layout_navegacion_total)

        btn_mostrar_stats = Button(text='Estadisticas', on_press=partial(self.boton_stats_total, usuario),
                                   height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_categoria = Button(text='Categoria', on_press=partial(self.boton_categoria_total, usuario),
                                       height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_gastos = Button(text='Gastos', on_press=partial(self.boton_gastos_total, usuario),
                                    height=Window.height * 0.05, size_hint_y=None)

        self.layout_botones_total.add_widget(btn_mostrar_stats)
        self.layout_botones_total.add_widget(btn_mostrar_categoria)
        self.layout_botones_total.add_widget(btn_mostrar_gastos)
        self.layout_total.add_widget(self.layout_botones_total)

        self.layout_total.add_widget(self.layout_stats_total)
        self.main_layout.add_widget(self.layout_total)

    def boton_stats_total(self, usuario, instance):
        if len(self.layout_stats_total.children) > 0:
            self.layout_stats_total.clear_widgets()
            self.altura = 0.21
        else:
            self.mostrar_stats_total(usuario)

    def boton_categoria_total(self, usuario, instance):
        if len(self.layout_stats_total.children) > 0:
            self.layout_stats_total.clear_widgets()
            self.altura = 0.21
        else:
            self.mostrar_gasto_categorias_total(usuario)

    def boton_gastos_total(self, usuario, instance):
        if len(self.layout_stats_total.children) > 0:
            self.layout_stats_total.clear_widgets()
            self.altura = 0.21
        else:
            self.mostrar_gastos_total(usuario)

    def mostrar_stats_total(self, usuario):
        clase_calc = Calculos()
        gasto_actual, ingresos_actual = clase_calc.calcular_saldo_total(usuario)
        gasto_ing = clase_calc.calcular_gasto_ing_total(usuario)
        gasto_ahorros = clase_calc.calcular_gasto_ahorros_total(usuario)
        saldo_actual = ingresos_actual - gasto_actual
        alquiler_total = clase_calc.calcular_alquiler_total(usuario)
        gasto_viajes = clase_calc.calcular_gasto_viajes_total(usuario)
        gasto_sin_viajes = gasto_actual - gasto_viajes

        self.layout_saldo_total = GridLayout(cols=2, height=Window.height * 0.15,
                                             size_hint_y=None)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_actual, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_ingreso = Label(text="Ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_ingreso = Label(text=str(round(ingresos_actual, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_saldo = Label(text="Saldo (total):", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo = Label(text=str(round(saldo_actual, 2)) + " €", height=Window.height * 0.05,
                            size_hint_y=None)

        nombre_saldo_ing = Label(text="Saldo (ingresos):", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo_ing = Label(text=str(round(ingresos_actual-gasto_ing, 2)) + " €", height=Window.height * 0.05,
                            size_hint_y=None)

        nombre_alquiler = Label(text="Alquiler:", height=Window.height * 0.05, size_hint_y=None)
        valor_alquiler = Label(text=str(round(alquiler_total, 2)) + " €", height=Window.height * 0.05,
                               size_hint_y=None)

        nombre_sin_alquiler = Label(text="Gasto sin alquiler:", height=Window.height * 0.05, size_hint_y=None)
        valor_sin_alquiler = Label(text=str(round(gasto_actual - alquiler_total, 2)) + " €",
                                   height=Window.height * 0.05,
                                   size_hint_y=None)

        nombre_gasto_ing = Label(text="Gasto procedente de ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto_ing = Label(text=str(round(gasto_ing, 2)) + " €", height=Window.height * 0.05,
                                size_hint_y=None)

        nombre_gasto_ahorros = Label(text="Gasto procedente de ahorros:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto_ahorros = Label(text=str(round(gasto_ahorros, 2)) + " €", height=Window.height * 0.05,
                                    size_hint_y=None)

        nombre_gasto_sin_viajes = Label(text="Gastos sin viajes:", height=Window.height * 0.05,
                                        size_hint_y=None)
        valor_gasto_sin_viajes = Label(text=str(round(gasto_sin_viajes, 2)) + " €", height=Window.height * 0.05,
                                       size_hint_y=None)

        self.layout_saldo_total.add_widget(nombre_ingreso)
        self.layout_saldo_total.add_widget(valor_ingreso)

        self.layout_saldo_total.add_widget(nombre_gasto)
        self.layout_saldo_total.add_widget(valor_gasto)

        self.layout_saldo_total.add_widget(nombre_saldo)
        self.layout_saldo_total.add_widget(valor_saldo)

        self.layout_saldo_total.add_widget(nombre_saldo_ing)
        self.layout_saldo_total.add_widget(valor_saldo_ing)

        self.layout_saldo_total.add_widget(nombre_alquiler)
        self.layout_saldo_total.add_widget(valor_alquiler)

        self.layout_saldo_total.add_widget(nombre_sin_alquiler)
        self.layout_saldo_total.add_widget(valor_sin_alquiler)

        self.layout_saldo_total.add_widget(nombre_gasto_ing)
        self.layout_saldo_total.add_widget(valor_gasto_ing)

        self.layout_saldo_total.add_widget(nombre_gasto_ahorros)
        self.layout_saldo_total.add_widget(valor_gasto_ahorros)

        self.layout_saldo_total.add_widget(nombre_gasto_sin_viajes)
        self.layout_saldo_total.add_widget(valor_gasto_sin_viajes)

        self.layout_stats_total.add_widget(self.layout_saldo_total)

    def mostrar_gasto_categorias_total(self, usuario):
        clase_calc = Calculos()
        self.layout_encabezados_categoria_total = GridLayout(cols=4, height=Window.height * 0.05, size_hint_y=None)
        gasto_total, ingresos_total = clase_calc.calcular_saldo_total(usuario)
        alquiler_total = clase_calc.calcular_alquiler_total(usuario)

        encabezado_categoria = Label(text="Categoria", height=Window.height * 0.05, size_hint_y=None)
        encabezado_gasto = Label(text="Gasto", height=Window.height * 0.05, size_hint_y=None)
        encabezado_porcentaje = Label(text="%", height=Window.height * 0.05, size_hint_y=None)
        encabezado_por_sin_alq = Label(text="% sin alquiler", height=Window.height * 0.05, size_hint_y=None)
        self.layout_encabezados_categoria_total.add_widget(encabezado_categoria)
        self.layout_encabezados_categoria_total.add_widget(encabezado_gasto)
        self.layout_encabezados_categoria_total.add_widget(encabezado_porcentaje)
        self.layout_encabezados_categoria_total.add_widget(encabezado_por_sin_alq)
        self.layout_stats_total.add_widget(self.layout_encabezados_categoria_total)

        for i in range(len(categorias)):
            self.layout_categoria_total = GridLayout(cols=4, height=Window.height * 0.05, size_hint_y=None)
            gasto_categoria = 0
            with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if row and row[2] == categorias[i]:
                        gasto_categoria += round(float(row[3]), 2)
            if gasto_categoria > 0:
                nombre = Label(text=categorias[i], height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_total.add_widget(nombre)
                valor = Label(text=str(round(gasto_categoria, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_total.add_widget(valor)
                porcentaje = Label(text=str(round(gasto_categoria / gasto_total * 100, 2)) + "%",
                                   height=Window.height * 0.05,
                                   size_hint_y=None)
                self.layout_categoria_total.add_widget(porcentaje)
                if categorias[i] != "Alquiler":
                    porcentaje_sin_alquiler = Label(
                        text=str(round(gasto_categoria / (gasto_total - alquiler_total) * 100, 2)) + "%",
                        height=Window.height * 0.05,
                        size_hint_y=None)
                else:
                    porcentaje_sin_alquiler = Label(
                        text="",
                        height=Window.height * 0.05,
                        size_hint_y=None)
                self.layout_categoria_total.add_widget(porcentaje_sin_alquiler)
                self.layout_stats_total.add_widget(self.layout_categoria_total)

    def mostrar_gastos_total(self, usuario):
        self.layout_gastos_total = GridLayout(cols=1)
        self.layout_botones_buscar_total = GridLayout(cols=2, size_hint_y=None, height=Window.height * 0.05)
        self.scrollview_total = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)
        self.layout_lista_gastos_total = GridLayout(cols=5, size_hint_y=None)
        self.layout_lista_gastos_total.bind(minimum_height=self.layout_lista_gastos_total.setter('height'))
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
        self.layout_botones_buscar_total.add_widget(self.mainbutton_categoria)

        btn_buscar = Button(text="Buscar", on_press=partial(self.buscar_gastos_total, usuario),
                            size_hint_y=None, height=Window.height * 0.05)
        self.layout_botones_buscar_total.add_widget(btn_buscar)
        self.layout_gastos_total.add_widget(self.layout_botones_buscar_total)
        self.layout_stats_total.add_widget(self.layout_gastos_total)

    def buscar_gastos_total(self, usuario, instance):
        if len(self.layout_lista_gastos_total.children) > 0:
            self.layout_gastos_total.remove_widget(self.scrollview_total)
            self.scrollview_total.remove_widget(self.layout_lista_gastos_total)
            self.layout_lista_gastos_total.clear_widgets()
            self.altura = 0.21
        else:
            self.mostrar_lista_gastos_total(usuario)

    def mostrar_lista_gastos_total(self, usuario):
        cat = self.mainbutton_categoria.text
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if cat == "Categoria":
                    if row:
                        label_fecha_total = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_total = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_total = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_total = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_total = Label(text=row[4], height=Window.height * 0.05, size_hint_y=None)

                        self.layout_lista_gastos_total.add_widget(label_fecha_total)
                        self.layout_lista_gastos_total.add_widget(label_concepto_total)
                        self.layout_lista_gastos_total.add_widget(label_categoria_total)
                        self.layout_lista_gastos_total.add_widget(label_precio_total)
                        self.layout_lista_gastos_total.add_widget(label_fuente_total)
                else:
                    if row and row[2] == cat:
                        label_fecha_total = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_total = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_total = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_total = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_total = Label(text=row[4], height=Window.height * 0.05, size_hint_y=None)

                        self.layout_lista_gastos_total.add_widget(label_fecha_total)
                        self.layout_lista_gastos_total.add_widget(label_concepto_total)
                        self.layout_lista_gastos_total.add_widget(label_categoria_total)
                        self.layout_lista_gastos_total.add_widget(label_precio_total)
                        self.layout_lista_gastos_total.add_widget(label_fuente_total)

        if len(self.layout_lista_gastos_total.children) == 0:
            label_no_gastos = Label(text="No hay gastos", height=Window.height * 0.05, size_hint_y=None)
            self.layout_lista_gastos_total.add_widget(label_no_gastos)

        self.scrollview_total.add_widget(self.layout_lista_gastos_total)
        self.layout_gastos_total.add_widget(self.scrollview_total)

    def boton_volver_total(self, instance):
        self.main_layout.remove_widget(self.layout_total)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()