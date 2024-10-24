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
              "Alquiler", "Viajes", "Coche"]


class AnadirGasto:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.31

    def menu_anadir_gasto(self, usuario):
        self.layout_anadir_gasto = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_inputs_anadir_gasto = GridLayout(cols=5, height=Window.height * 0.05, size_hint_y=None)
        self.layout_navegacion_anadir_gasto = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_anadir_gasto), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_anadir_gasto.add_widget(btn_exit)
        self.layout_navegacion_anadir_gasto.add_widget(btn_volver)
        self.layout_anadir_gasto.add_widget(self.layout_navegacion_anadir_gasto)

        self.dropdown_categoria = DropDown()
        for cat in categorias:
            btn = Button(text=cat, size_hint_y=None, height=Window.height * 0.05)
            btn.bind(on_release=lambda btn: self.dropdown_categoria.select(btn.text))
            self.dropdown_categoria.add_widget(btn)
        self.mainbutton_categoria = Button(text='Categoria', height=Window.height * 0.05, size_hint_y=None)
        self.mainbutton_categoria.bind(on_release=self.dropdown_categoria.open)
        self.dropdown_categoria.bind(on_select=lambda instance, x: setattr(self.mainbutton_categoria, 'text', x))

        self.input_fecha = TextInput(hint_text='(dd/mm/yyyy)', multiline=False,
                                     height=Window.height * 0.05, size_hint_y=None)
        self.input_concepto = TextInput(hint_text='Concepto', multiline=False,
                                        height=Window.height * 0.05, size_hint_y=None)
        self.input_precio = TextInput(hint_text='Precio', multiline=False,
                                      height=Window.height * 0.05, size_hint_y=None, size_hint_x=0.6)

        self.input_fuente = TextInput(hint_text='Fuente', multiline=False,
                                      height=Window.height * 0.05, size_hint_y=None, size_hint_x=0.6)

        self.layout_inputs_anadir_gasto.add_widget(self.input_fecha)
        self.layout_inputs_anadir_gasto.add_widget(self.input_concepto)
        self.layout_inputs_anadir_gasto.add_widget(self.mainbutton_categoria)
        self.layout_inputs_anadir_gasto.add_widget(self.input_precio)
        self.layout_inputs_anadir_gasto.add_widget(self.input_fuente)
        self.layout_anadir_gasto.add_widget(self.layout_inputs_anadir_gasto)

        btn_anadir = Button(text='Añadir gasto', on_press=partial(self.anadir_gasto, usuario),
                            height=Window.height * 0.05, size_hint_y=None)

        self.layout_anadir_gasto.add_widget(btn_anadir)
        self.main_layout.add_widget(self.layout_anadir_gasto)


    def anadir_gasto(self, usuario, instance):
        fecha = self.input_fecha.text
        con = self.input_concepto.text
        cat = self.mainbutton_categoria.text
        pre = self.input_precio.text
        fue = self.input_fuente.text
        with open(usuario + "/gastos"+"_"+usuario+".csv", mode='a', newline="\n") as csvfile:
            write = csv.writer(csvfile,delimiter = ",")
            write.writerow([fecha,con,cat,pre,fue])

        self.main_layout.remove_widget(self.layout_anadir_gasto)
        self.main_layout.add_widget(self.main_page)


    def boton_volver_anadir_gasto(self, instance):
        self.main_layout.remove_widget(self.layout_anadir_gasto)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()