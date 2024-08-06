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


class AnadirIngreso:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.31

    def menu_anadir_ingreso(self, usuario):
        self.layout_anadir_ingreso = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_inputs_anadir_ingreso = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_navegacion_anadir_ingreso = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_anadir_ingreso), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_anadir_ingreso.add_widget(btn_exit)
        self.layout_navegacion_anadir_ingreso.add_widget(btn_volver)
        self.layout_anadir_ingreso.add_widget(self.layout_navegacion_anadir_ingreso)

        self.input_fecha = TextInput(hint_text='(dd/mm/yyyy)', multiline=False,
                                     height=Window.height * 0.05, size_hint_y=None)
        self.input_importe = TextInput(hint_text='Importe', multiline=False,
                                       height=Window.height * 0.05, size_hint_y=None)

        self.layout_inputs_anadir_ingreso.add_widget(self.input_fecha)
        self.layout_inputs_anadir_ingreso.add_widget(self.input_importe)
        self.layout_anadir_ingreso.add_widget(self.layout_inputs_anadir_ingreso)

        btn_anadir = Button(text='Añadir ingreso', on_press=partial(self.anadir_ingreso, usuario),
                            height=Window.height * 0.05, size_hint_y=None)


        self.layout_anadir_ingreso.add_widget(btn_anadir)
        self.main_layout.add_widget(self.layout_anadir_ingreso)


    def anadir_ingreso(self, usuario, instance):
        fecha = self.input_fecha.text
        importe = self.input_importe.text
        with open(usuario + "/ingresos"+"_"+usuario+".csv", mode='a', newline="\n") as csvfile:
            write = csv.writer(csvfile,delimiter = ",")
            write.writerow([fecha,importe])

        self.main_layout.remove_widget(self.layout_anadir_ingreso)
        self.main_layout.add_widget(self.main_page)


    def boton_volver_anadir_ingreso(self, instance):
        self.main_layout.remove_widget(self.layout_anadir_ingreso)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()