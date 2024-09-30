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

categorias = ["Gasolina", "Hogar", "Transporte", "Dulces", "Ocio",
              "Caprichos", "Comida", "Restaurantes", "Medicamentos",
              "Alquiler", "Viajes"]


class Viajes:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.05

    def menu_viajes(self, usuario):
        self.layout_stats_viajes = GridLayout(cols=1)
        self.layout_viajes = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_navegacion_viajes = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.scrollview_data_viajes = ScrollView(height = Window.height * (1 - self.altura), size_hint_y = None)
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
        self.layout_viajes.remove_widget(self.scrollview_data_viajes)
        self.layout_botones_viajes = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)
        self.layout_viajes.add_widget(self.layout_botones_viajes)

        btn_mostrar_stats = Button(text='Estadisticas', on_press = partial(self.boton_stats_viajes, usuario, viaje),
                                   height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_categoria = Button(text='Categoria',
                                       height=Window.height * 0.05, size_hint_y=None)

        btn_mostrar_gastos = Button(text='Gastos',
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

    def boton_volver_viajes(self, instance):
        self.main_layout.remove_widget(self.layout_viajes)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()