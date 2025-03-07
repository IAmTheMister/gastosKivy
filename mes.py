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
              "Alquiler", "Viajes", "Coche","Merienda"]


class Mes:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.27

    def menu_mes(self,usuario):
        self.layout_mes = GridLayout(cols=1, spacing=10, height = Window.height)

        self.layout_stats_mes = GridLayout(cols=1)
        self.layout_navegacion_mes = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_inputs_mes = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_botones_mes = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_mes), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_mes.add_widget(btn_exit)
        self.layout_navegacion_mes.add_widget(btn_volver)
        self.layout_mes.add_widget(self.layout_navegacion_mes)

        self.input_ano = TextInput(hint_text='Año (yyyy)', multiline=False,
                                   height=Window.height * 0.05, size_hint_y=None)
        self.input_mes = TextInput(hint_text='Mes (mm)', multiline=False, height=Window.height * 0.05,
                                   size_hint_y=None)

        self.layout_inputs_mes.add_widget(self.input_mes)
        self.layout_inputs_mes.add_widget(self.input_ano)
        self.layout_mes.add_widget(self.layout_inputs_mes)

        btn_mostrar_stats = Button(text='Estadísticas', on_press=partial(self.boton_stats_mes, usuario),
                                   height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_categoria = Button(text='Categoria', on_press=partial(self.boton_categoria_mes, usuario),
                                       height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_gastos = Button(text='Gastos', on_press=partial(self.boton_gastos_mes, usuario),
                                    height=Window.height * 0.05, size_hint_y=None)

        self.layout_botones_mes.add_widget(btn_mostrar_stats)
        self.layout_botones_mes.add_widget(btn_mostrar_categoria)
        self.layout_botones_mes.add_widget(btn_mostrar_gastos)
        self.layout_mes.add_widget(self.layout_botones_mes)

        self.layout_mes.add_widget(self.layout_stats_mes)
        self.main_layout.add_widget(self.layout_mes)

    def boton_stats_mes(self, usuario, instance):
        if len(self.layout_stats_mes.children) > 0:
            self.layout_stats_mes.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_stats_mes(usuario)

    def boton_categoria_mes(self, usuario, instance):
        if len(self.layout_stats_mes.children) > 0:
            self.layout_stats_mes.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_gasto_categorias_mes(usuario)

    def boton_gastos_mes(self, usuario, instance):
        if len(self.layout_stats_mes.children) > 0:
            self.layout_stats_mes.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_gastos_mes(usuario)

    def mostrar_stats_mes(self, usuario):
        clase_calc = Calculos()
        ano_actual = int(self.input_ano.text)
        mes_actual = int(self.input_mes.text)
        gasto_actual, ingresos_actual = clase_calc.calcular_saldo_mes(usuario,ano_actual, mes_actual)
        gasto_ing = clase_calc.calcular_gasto_ing_mes(usuario, ano_actual, mes_actual)
        gasto_ahorros = clase_calc.calcular_gasto_ahorros_mes(usuario, ano_actual, mes_actual)
        saldo_actual = ingresos_actual - gasto_actual
        alquiler_mes = clase_calc.calcular_alquiler_mes(usuario,ano_actual, mes_actual)
        gasto_viajes = clase_calc.calcular_gasto_viajes_mes(usuario,ano_actual, mes_actual)
        gasto_sin_viajes = gasto_actual - gasto_viajes
        self.layout_saldo_mes = GridLayout(cols=2, height=Window.height * 0.15,
                                           size_hint_y=None)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_actual, 2))+" €", height=Window.height * 0.05, size_hint_y=None)

        nombre_ingreso = Label(text="Ingresos:", height=Window.height * 0.05, size_hint_y=None)
        valor_ingreso = Label(text=str(round(ingresos_actual, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_saldo = Label(text="Saldo (total):", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo = Label(text=str(round(saldo_actual, 2)) + " €", height=Window.height * 0.05,
                            size_hint_y=None)

        nombre_saldo_ing = Label(text="Saldo (ingresos):", height=Window.height * 0.05, size_hint_y=None)
        valor_saldo_ing = Label(text=str(round(ingresos_actual - gasto_ing, 2)) + " €", height=Window.height * 0.05,
                                size_hint_y=None)

        nombre_alquiler = Label(text="Alquiler:", height=Window.height * 0.05, size_hint_y=None)
        valor_alquiler = Label(text=str(round(alquiler_mes, 2)) + " €", height=Window.height * 0.05,
                            size_hint_y=None)

        nombre_sin_alquiler = Label(text="Gasto sin alquiler:", height=Window.height * 0.05, size_hint_y=None)
        valor_sin_alquiler = Label(text=str(round(gasto_actual-alquiler_mes, 2)) + " €", height=Window.height * 0.05,
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

        self.layout_saldo_mes.add_widget(nombre_ingreso)
        self.layout_saldo_mes.add_widget(valor_ingreso)

        self.layout_saldo_mes.add_widget(nombre_gasto)
        self.layout_saldo_mes.add_widget(valor_gasto)

        self.layout_saldo_mes.add_widget(nombre_saldo)
        self.layout_saldo_mes.add_widget(valor_saldo)

        self.layout_saldo_mes.add_widget(nombre_saldo_ing)
        self.layout_saldo_mes.add_widget(valor_saldo_ing)

        self.layout_saldo_mes.add_widget(nombre_alquiler)
        self.layout_saldo_mes.add_widget(valor_alquiler)

        self.layout_saldo_mes.add_widget(nombre_sin_alquiler)
        self.layout_saldo_mes.add_widget(valor_sin_alquiler)

        self.layout_saldo_mes.add_widget(nombre_gasto_ing)
        self.layout_saldo_mes.add_widget(valor_gasto_ing)

        self.layout_saldo_mes.add_widget(nombre_gasto_ahorros)
        self.layout_saldo_mes.add_widget(valor_gasto_ahorros)

        self.layout_saldo_mes.add_widget(nombre_gasto_sin_viajes)
        self.layout_saldo_mes.add_widget(valor_gasto_sin_viajes)

        self.layout_stats_mes.add_widget(self.layout_saldo_mes)

    def mostrar_gasto_categorias_mes(self, usuario):
        clase_calc = Calculos()

        self.layout_mostrar_categoria_mes = GridLayout(cols=1, height=Window.height*1.5, size_hint_y=None)
        self.scrollview_categorias_mes = ScrollView(height=Window.height, size_hint_y=None)
        self.layout_encabezados_categoria_mes = GridLayout(cols=4, height=Window.height * 0.05, size_hint_y=None)
        self.layout_categorias_por_separado_mes = GridLayout(cols=4, height=Window.height * 0.9, size_hint_y=None)
        ano = int(self.input_ano.text)
        mes = int(self.input_mes.text)

        gasto_mes, ingresos_mes = clase_calc.calcular_saldo_mes(usuario, ano, mes)
        alquiler_mes = clase_calc.calcular_alquiler_mes(usuario, ano, mes)
        viajes_mes = clase_calc.calcular_gasto_viajes_mes(usuario, ano, mes)
        gasto_ingresos_mes = clase_calc.calcular_gasto_ing_mes(usuario, ano, mes)
        gasto_ahorros_mes = clase_calc.calcular_gasto_ahorros_mes(usuario, ano, mes)

        encabezado_grupos = Label(text="Categorías agrupadas",
                                  height=Window.height * 0.05,
                                  size_hint_y=None)
        self.layout_mostrar_categoria_mes.add_widget(encabezado_grupos)

        gasto_comida = clase_calc.calcular_gasto_rel_comida_mes(usuario, ano, mes)
        gasto_ocio = clase_calc.calcular_gasto_rel_ocio_mes(usuario, ano, mes)
        gasto_transporte = clase_calc.calcular_gasto_rel_transporte_mes(usuario, ano, mes)
        gasto_resto = clase_calc.calcular_gasto_rel_resto_mes(usuario, ano, mes)

        layout_grupos_mes = GridLayout(cols=3, height=Window.height * 0.3, size_hint_y=None)

        label_rel_comida_mes = Label(text="Relacionado con comida:",
                                     height=Window.height * 0.05,
                                     size_hint_y=None)
        valor_rel_comida_mes = Label(text=str(round(gasto_comida, 2)) + " €",
                                     height=Window.height * 0.05,
                                     size_hint_y=None)
        porcentaje_gasto_total_rel_comida = Label(text=str(round(gasto_comida/gasto_mes * 100, 2)) + " %",
                                             height=Window.height * 0.05,
                                             size_hint_y=None)

        layout_grupos_mes.add_widget(label_rel_comida_mes)
        layout_grupos_mes.add_widget(valor_rel_comida_mes)
        layout_grupos_mes.add_widget(porcentaje_gasto_total_rel_comida)

        label_rel_ocio_mes = Label(text="Relacionado con ocio:",
                                   height=Window.height * 0.05,
                                   size_hint_y=None)
        valor_rel_ocio_mes = Label(text=str(round(gasto_ocio, 2)) + " €",
                                   height=Window.height * 0.05,
                                   size_hint_y=None)
        porcentaje_gasto_total_rel_ocio = Label(text=str(round(gasto_ocio / gasto_mes * 100, 2)) + " %",
                                                  height=Window.height * 0.05,
                                                  size_hint_y=None)

        layout_grupos_mes.add_widget(label_rel_ocio_mes)
        layout_grupos_mes.add_widget(valor_rel_ocio_mes)
        layout_grupos_mes.add_widget(porcentaje_gasto_total_rel_ocio)

        label_rel_viajes_mes = Label(text="Viajes:",
                                     height=Window.height * 0.05,
                                     size_hint_y=None)
        valor_rel_viajes_mes = Label(text=str(round(viajes_mes, 2)) + " €",
                                     height=Window.height * 0.05,
                                     size_hint_y=None)
        porcentaje_gasto_total_rel_viajes = Label(text=str(round(viajes_mes / gasto_mes * 100, 2)) + " %",
                                                height=Window.height * 0.05,
                                                size_hint_y=None)

        layout_grupos_mes.add_widget(label_rel_viajes_mes)
        layout_grupos_mes.add_widget(valor_rel_viajes_mes)
        layout_grupos_mes.add_widget(porcentaje_gasto_total_rel_viajes)

        label_rel_transporte_mes = Label(text="Relacionado con transporte:",
                                         height=Window.height * 0.05,
                                         size_hint_y=None)
        valor_rel_transporte_mes = Label(text=str(round(gasto_transporte, 2)) + " €",
                                         height=Window.height * 0.05,
                                         size_hint_y=None)
        porcentaje_gasto_total_rel_transporte = Label(text=str(round(gasto_transporte / gasto_mes * 100, 2)) + " %",
                                                height=Window.height * 0.05,
                                                size_hint_y=None)

        layout_grupos_mes.add_widget(label_rel_transporte_mes)
        layout_grupos_mes.add_widget(valor_rel_transporte_mes)
        layout_grupos_mes.add_widget(porcentaje_gasto_total_rel_transporte)

        label_rel_alquiler_mes = Label(text="Alquiler:",
                                       height=Window.height * 0.05,
                                       size_hint_y=None)
        valor_rel_alquiler_mes = Label(text=str(round(alquiler_mes, 2)) + " €",
                                       height=Window.height * 0.05,
                                       size_hint_y=None)
        porcentaje_gasto_total_rel_alquiler = Label(text=str(round(alquiler_mes / gasto_mes * 100, 2)) + " %",
                                                      height=Window.height * 0.05,
                                                      size_hint_y=None)

        layout_grupos_mes.add_widget(label_rel_alquiler_mes)
        layout_grupos_mes.add_widget(valor_rel_alquiler_mes)
        layout_grupos_mes.add_widget(porcentaje_gasto_total_rel_alquiler)

        label_rel_resto_mes = Label(text="Resto de gastos:",
                                    height=Window.height * 0.05,
                                    size_hint_y=None)
        valor_rel_resto_mes = Label(text=str(round(gasto_resto, 2)) + " €",
                                    height=Window.height * 0.05,
                                    size_hint_y=None)
        porcentaje_gasto_total_rel_resto = Label(text=str(round(gasto_resto / gasto_mes * 100, 2)) + " %",
                                                      height=Window.height * 0.05,
                                                      size_hint_y=None)

        layout_grupos_mes.add_widget(label_rel_resto_mes)
        layout_grupos_mes.add_widget(valor_rel_resto_mes)
        layout_grupos_mes.add_widget(porcentaje_gasto_total_rel_resto)

        self.layout_mostrar_categoria_mes.add_widget(layout_grupos_mes)



        encabezado_separados = Label(text="Categorías separadas",
                                  height=Window.height * 0.05,
                                  size_hint_y=None)
        self.layout_mostrar_categoria_mes.add_widget(encabezado_separados)

        encabezado_ingresos = Label(text="Ingresos",
                                     height=Window.height * 0.05,
                                     size_hint_y=None)
        self.layout_mostrar_categoria_mes.add_widget(encabezado_ingresos)

        encabezado_categoria = Label(text="Categoría", height=Window.height * 0.05, size_hint_y=None)
        encabezado_gasto = Label(text="Gasto", height=Window.height * 0.05, size_hint_y=None)
        encabezado_porcentaje = Label(text="%", height=Window.height * 0.05, size_hint_y=None)
        encabezado_por_sin_alq = Label(text="% sin alquiler", height=Window.height * 0.05, size_hint_y=None)

        self.layout_encabezados_categoria_mes.add_widget(encabezado_categoria)
        self.layout_encabezados_categoria_mes.add_widget(encabezado_gasto)
        self.layout_encabezados_categoria_mes.add_widget(encabezado_porcentaje)
        self.layout_encabezados_categoria_mes.add_widget(encabezado_por_sin_alq)

        self.layout_mostrar_categoria_mes.add_widget(self.layout_encabezados_categoria_mes)

        for i in range(len(categorias)):
            self.layout_categoria_mes = GridLayout(cols=4, height=Window.height * 0.05, size_hint_y=None)
            gasto_categoria = 0
            with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                    if row and row[2] == categorias[i] and fecha_row.year == ano and fecha_row.month == mes and row[4] == "Ingresos":
                        gasto_categoria += round(float(row[3]), 2)
            if gasto_categoria > 0:
                nombre = Label(text=categorias[i], height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_mes.add_widget(nombre)
                valor = Label(text=str(round(gasto_categoria, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_mes.add_widget(valor)
                porcentaje = Label(text=str(round(gasto_categoria / gasto_ingresos_mes * 100, 2)) + "%",
                                   height=Window.height * 0.05,
                                   size_hint_y=None)
                self.layout_categoria_mes.add_widget(porcentaje)
                if categorias[i] != "Alquiler":
                    porcentaje_sin_alquiler = Label(
                        text=str(round(gasto_categoria / (gasto_ingresos_mes - alquiler_mes) * 100, 2)) + "%",
                        height=Window.height * 0.05,
                        size_hint_y=None)
                else:
                    porcentaje_sin_alquiler = Label(
                        text="",
                        height=Window.height * 0.05,
                        size_hint_y=None)
                self.layout_categoria_mes.add_widget(porcentaje_sin_alquiler)
                self.layout_mostrar_categoria_mes.add_widget(self.layout_categoria_mes)

        encabezado_ahorros = Label(text="Ahorros",
                                    height=Window.height * 0.05,
                                    size_hint_y=None)
        self.layout_mostrar_categoria_mes.add_widget(encabezado_ahorros)

        for i in range(len(categorias)):
            self.layout_categoria_mes = GridLayout(cols=4, height=Window.height * 0.05, size_hint_y=None)
            gasto_categoria = 0
            with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                    if row and row[2] == categorias[i] and fecha_row.year == ano and fecha_row.month == mes and row[4] == "Ahorros":
                        gasto_categoria += round(float(row[3]), 2)
            if gasto_categoria > 0:
                nombre = Label(text=categorias[i], height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_mes.add_widget(nombre)
                valor = Label(text=str(round(gasto_categoria, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_mes.add_widget(valor)
                porcentaje = Label(text=str(round(gasto_categoria / gasto_ahorros_mes * 100, 2)) + "%",
                                   height=Window.height * 0.05,
                                   size_hint_y=None)
                self.layout_categoria_mes.add_widget(porcentaje)
                porcentaje_sin_alquiler = Label(
                        text="-",
                        height=Window.height * 0.05,
                        size_hint_y=None)

                self.layout_categoria_mes.add_widget(porcentaje_sin_alquiler)
                self.layout_mostrar_categoria_mes.add_widget(self.layout_categoria_mes)

        self.scrollview_categorias_mes.add_widget(self.layout_mostrar_categoria_mes)

        self.layout_stats_mes.add_widget(self.scrollview_categorias_mes)

        # self.layout_stats_mes.add_widget(self.layout_mostrar_categoria_mes)

    def mostrar_gastos_mes(self, usuario):
        self.layout_gastos_mes = GridLayout(cols=1)
        self.layout_botones_buscar_mes = GridLayout(cols=2, size_hint_y=None, height=Window.height * 0.05)
        self.scrollview_mes = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)
        self.layout_lista_gastos_mes = GridLayout(cols=5, size_hint_y=None)
        self.layout_lista_gastos_mes.bind(minimum_height=self.layout_lista_gastos_mes.setter('height'))
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
        self.layout_botones_buscar_mes.add_widget(self.mainbutton_categoria)

        btn_buscar = Button(text="Buscar", on_press=partial(self.buscar_gastos_mes, usuario),
                            size_hint_y=None, height=Window.height * 0.05)
        self.layout_botones_buscar_mes.add_widget(btn_buscar)
        self.layout_gastos_mes.add_widget(self.layout_botones_buscar_mes)
        self.layout_stats_mes.add_widget(self.layout_gastos_mes)

    def buscar_gastos_mes(self, usuario, instance):
        if len(self.layout_lista_gastos_mes.children) > 0:
            self.layout_gastos_mes.remove_widget(self.scrollview_mes)
            self.scrollview_mes.remove_widget(self.layout_lista_gastos_mes)
            self.layout_lista_gastos_mes.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_lista_gastos_mes(usuario)

    def mostrar_lista_gastos_mes(self, usuario):
        ano = int(self.input_ano.text)
        mes = int(self.input_mes.text)
        cat = self.mainbutton_categoria.text
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if cat == "Categoria":
                    if row and fecha_row.year == ano and fecha_row.month == mes:
                        label_fecha_mes = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_mes = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_mes = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_mes = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_mes = Label(text=row[4], height=Window.height * 0.05, size_hint_y=None)

                        self.layout_lista_gastos_mes.add_widget(label_fecha_mes)
                        self.layout_lista_gastos_mes.add_widget(label_concepto_mes)
                        self.layout_lista_gastos_mes.add_widget(label_categoria_mes)
                        self.layout_lista_gastos_mes.add_widget(label_precio_mes)
                        self.layout_lista_gastos_mes.add_widget(label_fuente_mes)
                else:
                    if row and fecha_row.year == ano and fecha_row.month == mes and row[2] == cat:
                        label_fecha_mes = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_mes = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_mes = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_mes = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)
                        label_fuente_mes = Label(text=row[4], height=Window.height * 0.05, size_hint_y=None)

                        self.layout_lista_gastos_mes.add_widget(label_fecha_mes)
                        self.layout_lista_gastos_mes.add_widget(label_concepto_mes)
                        self.layout_lista_gastos_mes.add_widget(label_categoria_mes)
                        self.layout_lista_gastos_mes.add_widget(label_precio_mes)
                        self.layout_lista_gastos_mes.add_widget(label_fuente_mes)

        if len(self.layout_lista_gastos_mes.children) == 0:
            label_no_gastos = Label(text = "No hay gastos", height=Window.height * 0.05, size_hint_y=None)
            self.layout_lista_gastos_mes.add_widget(label_no_gastos)

        self.scrollview_mes.add_widget(self.layout_lista_gastos_mes)
        self.layout_gastos_mes.add_widget(self.scrollview_mes)

    def boton_volver_mes(self, instance):
        self.main_layout.remove_widget(self.layout_mes)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()