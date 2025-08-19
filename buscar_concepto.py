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
              "Alquiler", "Viajes", "Coche", "Merienda", "Suministros"]

class BuscarConcepto:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.22

    def menu_concepto(self,usuario):
        self.layout_concepto = GridLayout(cols=1, spacing=10)


        self.layout_navegacion_concepto = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_botones_concepto = GridLayout(cols=3, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))
        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_concepto), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_concepto.add_widget(btn_exit)
        self.layout_navegacion_concepto.add_widget(btn_volver)
        self.layout_concepto.add_widget(self.layout_navegacion_concepto)

        self.layout_botones_buscar_concepto = GridLayout(cols=2, size_hint_y=None, height=Window.height * 0.05)
        self.scrollview_concepto = ScrollView(height=Window.height * (1 - self.altura), size_hint_y=None)
        self.layout_lista_gastos_concepto = GridLayout(cols=4, size_hint_y=None)
        self.layout_lista_gastos_concepto.bind(minimum_height=self.layout_lista_gastos_concepto.setter('height'))
        self.input_concepto = TextInput(hint_text="Concepto", size_hint_y=None, height=Window.height * 0.05)
        self.layout_botones_buscar_concepto.add_widget(self.input_concepto)

        btn_buscar = Button(text="Buscar", on_press=partial(self.buscar_gastos_concepto, usuario),
                            size_hint_y=None, height=Window.height * 0.05)
        self.layout_botones_buscar_concepto.add_widget(btn_buscar)
        self.layout_concepto.add_widget(self.layout_botones_buscar_concepto)

        self.main_layout.add_widget(self.layout_concepto)
        
    def buscar_gastos_concepto(self, usuario, instance):
        if len(self.layout_lista_gastos_concepto.children) > 0:
            self.layout_concepto.remove_widget(self.scrollview_concepto)
            self.scrollview_concepto.remove_widget(self.layout_lista_gastos_concepto)
            self.layout_lista_gastos_concepto.clear_widgets()
            self.altura = 0.22
        else:
            self.mostrar_lista_gastos_concepto(usuario)

    def mostrar_lista_gastos_concepto(self, usuario):
        concepto = self.input_concepto.text
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row and concepto in row[1]:
                    label_fecha_concepto = Label(text=row[0], height=Window.height * 0.05, size_hint_y=None)
                    label_concepto_concepto = Label(text=row[1], height=Window.height * 0.05, size_hint_y=None)
                    label_categoria_concepto = Label(text=row[2], height=Window.height * 0.05, size_hint_y=None)
                    label_precio_concepto = Label(text=row[3] + " €", height=Window.height * 0.05, size_hint_y=None)

                    self.layout_lista_gastos_concepto.add_widget(label_fecha_concepto)
                    self.layout_lista_gastos_concepto.add_widget(label_concepto_concepto)
                    self.layout_lista_gastos_concepto.add_widget(label_categoria_concepto)
                    self.layout_lista_gastos_concepto.add_widget(label_precio_concepto)

        if len(self.layout_lista_gastos_concepto.children) == 0:
            label_no_gastos = Label(text="No hay gastos", height=Window.height * 0.05, size_hint_y=None)
            self.layout_lista_gastos_concepto.add_widget(label_no_gastos)

        self.scrollview_concepto.add_widget(self.layout_lista_gastos_concepto)
        self.layout_concepto.add_widget(self.scrollview_concepto)
        
    def boton_volver_concepto(self, instance):
        self.main_layout.remove_widget(self.layout_concepto)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()