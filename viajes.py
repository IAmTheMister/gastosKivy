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

categorias = ["Gasolina", "Alojamiento", "Transporte", "Dulces", "Ocio", "Vuelos",
              "Souvenirs", "Comida", "Restaurantes", "Otros"]


class Viajes:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.05

    def menu_viajes(self, usuario):
        self.layout_stats_viajes = GridLayout(cols=1)
        self.layout_viajes = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_navegacion_viajes = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.scrollview_data_viajes = ScrollView(height = Window.height * (1 - 4 * self.altura), size_hint_y = None)
        self.layout_data_viajes = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        self.layout_data_viajes.bind(minimum_height=self.layout_data_viajes.setter('height'))

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_viajes), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_viajes.add_widget(btn_exit)
        self.layout_navegacion_viajes.add_widget(btn_volver)
        self.layout_viajes.add_widget(self.layout_navegacion_viajes)

        self.btn_anadir_gasto_viaje = Button(text='Añadir gasto', on_press = partial(self.pagina_anadir_gasto_viaje,usuario), height=Window.height * 0.1, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_viajes.add_widget(self.btn_anadir_gasto_viaje)

        self.main_layout.add_widget(self.layout_viajes)

        lista_viajes = self.get_lista_viajes(usuario)

        for i in range(len(lista_viajes)):
            data_row = lista_viajes[i]
            btn_viaje = Button(text=data_row, height=Window.height * 0.05, size_hint_y=None)
            btn_viaje.bind(on_press=partial(self.mostrar_viaje, usuario, data_row))
            self.layout_data_viajes.add_widget(btn_viaje)

        self.scrollview_data_viajes.add_widget(self.layout_data_viajes)
        self.layout_viajes.add_widget(self.scrollview_data_viajes)

    def mostrar_viaje(self, usuario, viaje, instance):
        self.layout_viajes.remove_widget(self.btn_anadir_gasto_viaje)
        self.layout_viajes.remove_widget(self.scrollview_data_viajes)
        self.layout_botones_viajes = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)
        self.layout_viajes.add_widget(self.layout_botones_viajes)

        btn_mostrar_stats = Button(text='Estadisticas', on_press = partial(self.boton_stats_viajes, usuario, viaje),
                                   height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_categoria = Button(text='Categoria', on_press = partial(self.categoria_viajes, usuario, viaje),
                                       height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_gastos = Button(text='Gastos', on_press = partial(self.gastos_viajes, usuario, viaje),
                                    height=Window.height * 0.05, size_hint_y=None)

        self.layout_botones_viajes.add_widget(btn_mostrar_stats)
        self.layout_botones_viajes.add_widget(btn_mostrar_categoria)
        self.layout_botones_viajes.add_widget(btn_mostrar_gastos)

        self.layout_viajes.add_widget(self.layout_stats_viajes)
        
        
    def boton_stats_viajes(self, usuario, viaje, instance):
        if len(self.layout_stats_viajes.children) > 0:
            self.layout_stats_viajes.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_stats_viajes(usuario, viaje)

    def mostrar_stats_viajes(self, usuario, viaje):
        self.layout_saldo_viajes = GridLayout(cols=2, height=Window.height * 0.15,
                                           size_hint_y=None)
        gasto_viaje, gasto_viaje_sin_gas = self.calcular_gasto_viaje(usuario, viaje)
        nombre_gasto = Label(text="Gasto total:", height=Window.height * 0.05, size_hint_y=None)
        valor_gasto = Label(text=str(round(gasto_viaje, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)

        nombre_sin_gas = Label(text="Gasto sin gasolina:", height=Window.height * 0.05, size_hint_y=None)
        valor_sin_gas = Label(text=str(round(gasto_viaje_sin_gas, 2)) +" €", height=Window.height * 0.05,
                                   size_hint_y=None)

        self.layout_saldo_viajes.add_widget(nombre_gasto)
        self.layout_saldo_viajes.add_widget(valor_gasto)

        self.layout_saldo_viajes.add_widget(nombre_sin_gas)
        self.layout_saldo_viajes.add_widget(valor_sin_gas)

        self.layout_stats_viajes.add_widget(self.layout_saldo_viajes)
        
    def categoria_viajes(self,usuario, viaje, instance):
        if len(self.layout_stats_viajes.children) > 0:
            self.layout_stats_viajes.clear_widgets()
        else:
            self.mostrar_gasto_categorias_viajes(usuario, viaje)

    def gastos_viajes(self,usuario, viaje, instance):
        if len(self.layout_stats_viajes.children) > 0:
            self.layout_stats_viajes.clear_widgets()
        else:
            self.mostrar_gastos_viajes(usuario, viaje)

    def mostrar_gasto_categorias_viajes(self, usuario, viaje):
        self.layout_encabezados_categoria_viajes = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)
        encabezado_categoria = Label(text="Categoría", height=Window.height * 0.05, size_hint_y=None)
        encabezado_gasto = Label(text="Gasto", height=Window.height * 0.05, size_hint_y=None)
        encabezado_porcentaje = Label(text="%", height=Window.height * 0.05, size_hint_y=None)
        self.layout_encabezados_categoria_viajes.add_widget(encabezado_categoria)
        self.layout_encabezados_categoria_viajes.add_widget(encabezado_gasto)
        self.layout_encabezados_categoria_viajes.add_widget(encabezado_porcentaje)
        self.layout_stats_viajes.add_widget(self.layout_encabezados_categoria_viajes)

        gasto_viaje, gasto_viaje_sin_gas = self.calcular_gasto_viaje(usuario, viaje)

        for i in range(len(categorias)):
            self.layout_categoria_viajes = GridLayout(cols=3, rows=1, height=Window.height * 0.05,
                                                         size_hint_y=None)
            gasto_categoría_viaje = 0
            with open(usuario + "/viajes" + "_" + usuario + ".csv", newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if row[4] == viaje and row[2] == categorias[i]:
                        gasto_categoría_viaje += round(float(row[3]), 2)
            if gasto_categoría_viaje > 0:
                nombre = Label(text=categorias[i], height=Window.height * 0.05, size_hint_y=None)
                valor = Label(text=str(round(gasto_categoría_viaje, 2)) + " €", height=Window.height * 0.05, size_hint_y=None)
                porcentaje = Label(text=str(round(gasto_categoría_viaje / gasto_viaje * 100, 2)) + "%",
                                   height=Window.height * 0.05, size_hint_y=None)
                self.layout_categoria_viajes.add_widget(nombre)
                self.layout_categoria_viajes.add_widget(valor)
                self.layout_categoria_viajes.add_widget(porcentaje)
                self.layout_stats_viajes.add_widget(self.layout_categoria_viajes)

    def mostrar_gastos_viajes(self, usuario, viaje):
        self.layout_gastos_viajes = GridLayout(cols=1)
        self.layout_botones_buscar_viajes = GridLayout(cols=2, size_hint_y=None, height=Window.height * 0.05)
        self.scrollview_viajes = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)
        self.layout_lista_gastos_viajes = GridLayout(cols=5, size_hint_y=None)
        self.layout_lista_gastos_viajes.bind(minimum_height=self.layout_lista_gastos_viajes.setter('height'))
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
        self.layout_botones_buscar_viajes.add_widget(self.mainbutton_categoria)

        btn_buscar = Button(text="Buscar", on_press=partial(self.buscar_gastos_viajes, usuario, viaje),
                            size_hint_y=None, height=Window.height * 0.05)
        self.layout_botones_buscar_viajes.add_widget(btn_buscar)
        self.layout_gastos_viajes.add_widget(self.layout_botones_buscar_viajes)
        self.layout_stats_viajes.add_widget(self.layout_gastos_viajes)

    def buscar_gastos_viajes(self, usuario, viaje, instance):
        if len(self.layout_lista_gastos_viajes.children) > 0:
            self.layout_gastos_viajes.remove_widget(self.scrollview_viajes)
            self.scrollview_viajes.remove_widget(self.layout_lista_gastos_viajes)
            self.layout_lista_gastos_viajes.clear_widgets()
            self.altura = 0.27
        else:
            self.mostrar_lista_gastos_viajes(usuario, viaje)

    def mostrar_lista_gastos_viajes(self, usuario, viaje):
        cat = self.mainbutton_categoria.text
        with open(usuario + "/viajes" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if cat == "Categoria":
                    if row[4] == viaje:
                        label_fecha_viajes = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_viajes = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_viajes = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_viajes = Label(text=row[3] + " €", height=Window.height * 0.05,
                                                       size_hint_y=None)
                        label_fuente_viajes = Label(text=row[4], height=Window.height * 0.05,
                                                       size_hint_y=None)

                        self.layout_lista_gastos_viajes.add_widget(label_fecha_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_concepto_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_categoria_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_precio_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_fuente_viajes)
                else:
                    if row[4] == viaje and row[2] == cat:
                        label_fecha_viajes = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                        label_concepto_viajes = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                        label_categoria_viajes = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                        label_precio_viajes = Label(text=row[3] + " €", height=Window.height * 0.05,
                                                       size_hint_y=None)
                        label_fuente_viajes = Label(text=row[4], height=Window.height * 0.05,
                                                       size_hint_y=None)

                        self.layout_lista_gastos_viajes.add_widget(label_fecha_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_concepto_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_categoria_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_precio_viajes)
                        self.layout_lista_gastos_viajes.add_widget(label_fuente_viajes)

        if len(self.layout_lista_gastos_viajes.children) == 0:
            label_no_gastos = Label(text="No hay gastos", height=Window.height * 0.05, size_hint_y=None)
            self.layout_lista_gastos_viajes.add_widget(label_no_gastos)

        self.scrollview_viajes.add_widget(self.layout_lista_gastos_viajes)
        self.layout_gastos_viajes.add_widget(self.scrollview_viajes)
            
            
#--------------------------------------------------------------------

    def calcular_gasto_viaje(self, usuario, viaje):
        gasto = 0
        gasto_sin_gasolina = 0
        with open(usuario + "/viajes"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row[4] == viaje:
                    gasto += float(row[3])
                    if row[3] != "Gasolina":
                        gasto_sin_gasolina += float(row[3])
        return gasto, gasto_sin_gasolina



    def get_lista_viajes(self, usuario):
        lista_viajes = []
        with open(usuario + "/viajes"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row[4] not in lista_viajes:
                    lista_viajes.append(row[4])
        return lista_viajes

    def pagina_anadir_gasto_viaje(self,usuario, instance):
        self.layout_viajes.remove_widget(self.layout_navegacion_viajes)
        self.layout_viajes.remove_widget(self.scrollview_data_viajes)
        self.layout_viajes.remove_widget(self.btn_anadir_gasto_viaje)
        self.menu_anadir_gasto_viaje(usuario)

    def menu_anadir_gasto_viaje(self, usuario):
        self.layout_anadir_gasto_viaje = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_inputs_anadir_gasto_viaje = GridLayout(cols=5, height=Window.height * 0.05, size_hint_y=None)
        self.layout_navegacion_anadir_gasto_viaje = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_anadir_gasto_viaje), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_anadir_gasto_viaje.add_widget(btn_exit)
        self.layout_navegacion_anadir_gasto_viaje.add_widget(btn_volver)
        self.layout_anadir_gasto_viaje.add_widget(self.layout_navegacion_anadir_gasto_viaje)

        self.dropdown_categoria_viaje = DropDown()
        for cat in categorias:
            btn = Button(text=cat, size_hint_y=None, height=Window.height * 0.05)
            btn.bind(on_release=lambda btn: self.dropdown_categoria_viaje.select(btn.text))
            self.dropdown_categoria_viaje.add_widget(btn)
        self.mainbutton_categoria_viaje = Button(text='Categoria', height=Window.height * 0.05, size_hint_y=None)
        self.mainbutton_categoria_viaje.bind(on_release=self.dropdown_categoria_viaje.open)
        self.dropdown_categoria_viaje.bind(on_select=lambda instance, x: setattr(self.mainbutton_categoria_viaje, 'text', x))

        self.input_fecha_viaje = TextInput(hint_text='(dd/mm/yyyy)', multiline=False,
                                     height=Window.height * 0.05, size_hint_y=None)
        self.input_concepto_viaje = TextInput(hint_text='Concepto', multiline=False,
                                        height=Window.height * 0.05, size_hint_y=None)
        self.input_precio_viaje = TextInput(hint_text='Precio', multiline=False,
                                      height=Window.height * 0.05, size_hint_y=None, size_hint_x=0.6)

        self.input_nombre_viaje = TextInput(hint_text='Viaje', multiline=False,
                                      height=Window.height * 0.05, size_hint_y=None, size_hint_x=0.6)

        self.layout_inputs_anadir_gasto_viaje.add_widget(self.input_fecha_viaje)
        self.layout_inputs_anadir_gasto_viaje.add_widget(self.input_concepto_viaje)
        self.layout_inputs_anadir_gasto_viaje.add_widget(self.mainbutton_categoria_viaje)
        self.layout_inputs_anadir_gasto_viaje.add_widget(self.input_precio_viaje)
        self.layout_inputs_anadir_gasto_viaje.add_widget(self.input_nombre_viaje)
        self.layout_anadir_gasto_viaje.add_widget(self.layout_inputs_anadir_gasto_viaje)

        btn_anadir = Button(text='Añadir gasto', on_press=partial(self.anadir_gasto_viaje, usuario),
                            height=Window.height * 0.05, size_hint_y=None)

        self.layout_anadir_gasto_viaje.add_widget(btn_anadir)
        self.layout_viajes.add_widget(self.layout_anadir_gasto_viaje)


    def anadir_gasto_viaje(self, usuario, instance):
        fecha = self.input_fecha_viaje.text
        con = self.input_concepto_viaje.text
        cat = self.mainbutton_categoria_viaje.text
        pre = self.input_precio_viaje.text
        nombre = self.input_nombre_viaje.text
        with open(usuario + "/viajes"+"_"+usuario+".csv", mode='a', newline="\n") as csvfile:
            write = csv.writer(csvfile,delimiter = ",")
            write.writerow([fecha,con,cat,pre,nombre])

        self.layout_viajes.remove_widget(self.layout_anadir_gasto_viaje)
        self.layout_viajes.add_widget(self.layout_navegacion_viajes)
        self.layout_viajes.add_widget(self.btn_anadir_gasto_viaje)
        self.layout_viajes.add_widget(self.scrollview_data_viajes)


    def boton_volver_anadir_gasto_viaje(self, instance):
        self.layout_viajes.remove_widget(self.layout_anadir_gasto_viaje)
        self.layout_viajes.add_widget(self.layout_navegacion_viajes)
        self.layout_viajes.add_widget(self.btn_anadir_gasto_viaje)
        self.layout_viajes.add_widget(self.scrollview_data_viajes)


    def boton_volver_viajes(self, instance):
        self.main_layout.remove_widget(self.layout_viajes)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()