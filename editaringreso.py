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
              "Alquiler", "Viajes", "Coche","Merienda"]


class EditarIngreso:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.05

    def menu_editar_ingreso(self, usuario):
        self.layout_editar_ingreso = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_navegacion_editar_ingreso = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.scrollview_data_editar_ingreso = ScrollView(height = Window.height * (1 - self.altura), size_hint_y = None)
        self.layout_data_editar_ingreso = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        self.layout_data_editar_ingreso.bind(minimum_height=self.layout_data_editar_ingreso.setter('height'))

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_editar_ingreso), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_editar_ingreso.add_widget(btn_exit)
        self.layout_navegacion_editar_ingreso.add_widget(btn_volver)
        self.layout_editar_ingreso.add_widget(self.layout_navegacion_editar_ingreso)

        self.data_list = []
        with open(usuario + "/ingresos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.data_list.append([row[0], row[1]])

        if len(self.data_list) > 3:
            for i in range(len(self.data_list)-3, len(self.data_list)):
                data_row = self.data_list[i]
                btn_ingreso = Button(text = data_row[0] + ": " + data_row[1], height=Window.height * 0.05, size_hint_y=None)
                btn_ingreso.bind(on_press=partial(self.editar_ingreso,usuario,data_row))
                self.layout_data_editar_ingreso.add_widget(btn_ingreso)
        else:
            for i in range(len(self.data_list)):
                data_row = self.data_list[i]
                btn_ingreso = Button(text = data_row[0] + ": " + data_row[1], height=Window.height * 0.05, size_hint_y=None)
                btn_ingreso.bind(on_press=partial(self.editar_ingreso,usuario,data_row))
                self.layout_data_editar_ingreso.add_widget(btn_ingreso)

        self.scrollview_data_editar_ingreso.add_widget(self.layout_data_editar_ingreso)
        self.layout_editar_ingreso.add_widget(self.scrollview_data_editar_ingreso)

        self.main_layout.add_widget(self.layout_editar_ingreso)

    def editar_ingreso(self, usuario, row,instance):
        self.main_layout.remove_widget(self.layout_editar_ingreso)
        self.layout_edicion_ingreso = GridLayout(cols = 1, spacing = 10)
        self.layout_ingreso_antiguo = GridLayout(cols = 2, height=Window.height * 0.05, size_hint_y = None)
        self.layout_ingreso_nuevo = GridLayout(cols= 2, height=Window.height * 0.05, size_hint_y=None)
        self.layout_navegacion_edicion_ingreso = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_edicion_ingreso),
                            height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_edicion_ingreso.add_widget(btn_exit)
        self.layout_navegacion_edicion_ingreso.add_widget(btn_volver)
        self.layout_edicion_ingreso.add_widget(self.layout_navegacion_edicion_ingreso)

        label_ingreso_ant = Label(text = "Ingreso antiguo", height=Window.height * 0.05, size_hint_y=None)
        self.layout_edicion_ingreso.add_widget(label_ingreso_ant)

        fecha_ant = Label(text = row[0], height=Window.height * 0.05, size_hint_y=None)
        importe_ant = Label(text = row[1], height=Window.height * 0.05, size_hint_y=None)
        self.layout_ingreso_antiguo.add_widget(fecha_ant)
        self.layout_ingreso_antiguo.add_widget(importe_ant)
        self.layout_edicion_ingreso.add_widget(self.layout_ingreso_antiguo)

        label_ingreso_nuevo = Label(text="Ingreso editado", height=Window.height * 0.05, size_hint_y=None)
        self.layout_edicion_ingreso.add_widget(label_ingreso_nuevo)

        self.fecha_nueva = TextInput(hint_text = "dd/mm/yyyy", height=Window.height * 0.05, size_hint_y=None)
        self.importe_nueva = TextInput(hint_text = "Importe", height=Window.height * 0.05, size_hint_y=None)
        self.layout_ingreso_nuevo.add_widget(self.fecha_nueva)
        self.layout_ingreso_nuevo.add_widget(self.importe_nueva)
        self.layout_edicion_ingreso.add_widget(self.layout_ingreso_nuevo)

        btn_editar_ingreso = Button(text = "Editar ingreso", height=Window.height * 0.05, size_hint_y=None,
                                  on_press = partial(self.sobreescribir_csv,usuario,row))
        self.layout_edicion_ingreso.add_widget(btn_editar_ingreso)

        btn_eliminar_ingreso = Button(text="Eliminar ingreso", height=Window.height * 0.05, size_hint_y=None,
                                  on_press=partial(self.eliminar_ingreso,usuario,row))
        self.layout_edicion_ingreso.add_widget(btn_eliminar_ingreso)

        self.main_layout.add_widget(self.layout_edicion_ingreso)

    def sobreescribir_csv(self, usuario, row,instance):
        row_nueva = [self.fecha_nueva.text, self.importe_nueva.text]
        for i in range(len(self.data_list)):
            if self.data_list[i] == row:
                self.data_list[i] = row_nueva

        with open(usuario + "/ingresos"+"_"+usuario+".csv", mode='w', newline="\n") as csvfile:
            write = csv.writer(csvfile,delimiter = ",")
            for fila in self.data_list:
                write.writerow(fila)

        self.main_layout.remove_widget(self.layout_edicion_ingreso)
        self.main_layout.add_widget(self.layout_editar_ingreso)

    def eliminar_ingreso(self, usuario, row,instance):
        modified_data = self.data_list.copy()
        for i in range(len(self.data_list)):
            if self.data_list[i] == row:
                modified_data.remove(row)

        with open(usuario + "/ingresos"+"_"+usuario+".csv", mode='w', newline="\n") as csvfile:
            write = csv.writer(csvfile,delimiter = ",")
            for fila in modified_data:
                write.writerow(fila)

        self.main_layout.remove_widget(self.layout_edicion_ingreso)
        self.main_layout.add_widget(self.layout_editar_ingreso)

    def boton_volver_editar_ingreso(self, instance):
        self.main_layout.remove_widget(self.layout_editar_ingreso)
        self.main_layout.add_widget(self.main_page)

    def boton_volver_edicion_ingreso(self, instance):
        self.main_layout.remove_widget(self.layout_edicion_ingreso)
        self.main_layout.add_widget(self.layout_editar_ingreso)

    def exit_app(self, instance):
        App.get_running_app().stop()