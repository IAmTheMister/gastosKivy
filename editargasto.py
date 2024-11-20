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


class EditarGasto:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.05

    def menu_editar_gasto(self, usuario):
        self.layout_editar_gasto = GridLayout(cols=1, spacing=10, height=Window.height)
        self.layout_navegacion_editar_gasto = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        self.scrollview_data_editar_gasto = ScrollView(height = Window.height * (1 - self.altura), size_hint_y = None)
        self.layout_data_editar_gasto = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        self.layout_data_editar_gasto.bind(minimum_height=self.layout_data_editar_gasto.setter('height'))

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_editar_gasto), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_editar_gasto.add_widget(btn_exit)
        self.layout_navegacion_editar_gasto.add_widget(btn_volver)
        self.layout_editar_gasto.add_widget(self.layout_navegacion_editar_gasto)

        self.data_list = []
        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.data_list.append([row[0], row[1], row[2], row[3],row[4]])

        if len(self.data_list) > 10:
            for i in range(len(self.data_list)-10, len(self.data_list)):
                data_row = self.data_list[i]
                btn_gasto = Button(text = data_row[0] + ": " + data_row[1], height=Window.height * 0.05, size_hint_y=None)
                btn_gasto.bind(on_press=partial(self.editar_gasto,usuario, data_row))
                self.layout_data_editar_gasto.add_widget(btn_gasto)
        else:
            for i in range(len(self.data_list)):
                data_row = self.data_list[i]
                btn_gasto = Button(text=data_row[0] + ": " + data_row[1], height=Window.height * 0.05, size_hint_y=None)
                btn_gasto.bind(on_press=partial(self.editar_gasto, usuario, data_row))
                self.layout_data_editar_gasto.add_widget(btn_gasto)

        self.scrollview_data_editar_gasto.add_widget(self.layout_data_editar_gasto)
        self.layout_editar_gasto.add_widget(self.scrollview_data_editar_gasto)

        self.main_layout.add_widget(self.layout_editar_gasto)

    def editar_gasto(self, usuario, row, instance):
        self.main_layout.remove_widget(self.layout_editar_gasto)
        self.layout_edicion_gasto = GridLayout(cols = 1, spacing = 10)
        self.layout_gasto_antiguo = GridLayout(cols = 5, height=Window.height * 0.05, size_hint_y = None)
        self.layout_gasto_nuevo = GridLayout(cols= 5, height=Window.height * 0.05, size_hint_y=None)
        self.layout_navegacion_edicion_gasto = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_edicion_gasto),
                            height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_edicion_gasto.add_widget(btn_exit)
        self.layout_navegacion_edicion_gasto.add_widget(btn_volver)
        self.layout_edicion_gasto.add_widget(self.layout_navegacion_edicion_gasto)

        label_gasto_ant = Label(text = "Gasto antiguo", height=Window.height * 0.05, size_hint_y=None)
        self.layout_edicion_gasto.add_widget(label_gasto_ant)

        fecha_ant = Label(text = row[0], height=Window.height * 0.05, size_hint_y=None)
        concepto_ant = Label(text = row[1], height=Window.height * 0.05, size_hint_y=None)
        categoria_ant = Label(text = row[2], height=Window.height * 0.05, size_hint_y=None)
        precio_ant = Label(text = row[3], height=Window.height * 0.05, size_hint_y=None)
        fuente_ant = Label(text = row[4], height=Window.height * 0.05, size_hint_y=None)
        self.layout_gasto_antiguo.add_widget(fecha_ant)
        self.layout_gasto_antiguo.add_widget(concepto_ant)
        self.layout_gasto_antiguo.add_widget(categoria_ant)
        self.layout_gasto_antiguo.add_widget(precio_ant)
        self.layout_gasto_antiguo.add_widget(fuente_ant)
        self.layout_edicion_gasto.add_widget(self.layout_gasto_antiguo)

        label_gasto_nuevo = Label(text="Gasto editado", height=Window.height * 0.05, size_hint_y=None)
        self.layout_edicion_gasto.add_widget(label_gasto_nuevo)

        self.dropdown_categoria = DropDown()
        for cat in categorias:
            btn = Button(text=cat, size_hint_y=None, height=Window.height * 0.05)
            btn.bind(on_release=lambda btn: self.dropdown_categoria.select(btn.text))
            self.dropdown_categoria.add_widget(btn)
        self.mainbutton_categoria = Button(text='Categoria', height=Window.height * 0.05, size_hint_y=None)
        self.mainbutton_categoria.bind(on_release=self.dropdown_categoria.open)
        self.dropdown_categoria.bind(on_select=lambda instance, x: setattr(self.mainbutton_categoria, 'text', x))

        self.fecha_nueva = TextInput(hint_text = "dd/mm/yyyy", height=Window.height * 0.05, size_hint_y=None)
        self.concepto_nueva = TextInput(hint_text = "Concepto", height=Window.height * 0.05, size_hint_y=None)
        self.precio_nueva = TextInput(hint_text = "Precio", height=Window.height * 0.05, size_hint_y=None)
        self.fuente_nueva = TextInput(hint_text="Fuente", height=Window.height * 0.05, size_hint_y=None)
        self.layout_gasto_nuevo.add_widget(self.fecha_nueva)
        self.layout_gasto_nuevo.add_widget(self.concepto_nueva)
        self.layout_gasto_nuevo.add_widget(self.mainbutton_categoria)
        self.layout_gasto_nuevo.add_widget(self.precio_nueva)
        self.layout_gasto_nuevo.add_widget(self.fuente_nueva)
        self.layout_edicion_gasto.add_widget(self.layout_gasto_nuevo)

        btn_editar_gasto = Button(text = "Editar gasto", height=Window.height * 0.05, size_hint_y=None,
                                  on_press =partial(self.sobreescribir_csv,usuario, row))
        self.layout_edicion_gasto.add_widget(btn_editar_gasto)

        btn_eliminar_gasto = Button(text="Eliminar gasto", height=Window.height * 0.05, size_hint_y=None,
                                  on_press=partial(self.eliminar_gasto,usuario,row))
        self.layout_edicion_gasto.add_widget(btn_eliminar_gasto)

        self.main_layout.add_widget(self.layout_edicion_gasto)

    def sobreescribir_csv(self, usuario, row,instance):
        row_nueva = [self.fecha_nueva.text, self.concepto_nueva.text, self.mainbutton_categoria.text,
                     self.precio_nueva.text, self.fuente_nueva.text]
        for i in range(len(self.data_list)):
            if self.data_list[i] == row:
                self.data_list[i] = row_nueva

        with open(usuario + "/gastos"+"_"+usuario+".csv", mode='w', newline="\n") as csvfile:
            write = csv.writer(csvfile,delimiter = ",")
            for fila in self.data_list:
                write.writerow(fila)

        self.main_layout.remove_widget(self.layout_edicion_gasto)
        self.main_layout.add_widget(self.layout_editar_gasto)

    def eliminar_gasto(self, usuario, row, instance):
        modified_data = self.data_list.copy()
        for i in range(len(self.data_list)):
            if self.data_list[i] == row:
                modified_data.remove(row)

        with open(usuario + "/gastos"+"_"+usuario+".csv", mode='w', newline="\n") as csvfile:
            write = csv.writer(csvfile,delimiter = ",")
            for fila in modified_data:
                write.writerow(fila)

        self.main_layout.remove_widget(self.layout_edicion_gasto)
        self.main_layout.add_widget(self.layout_editar_gasto)

    def boton_volver_editar_gasto(self, instance):
        self.main_layout.remove_widget(self.layout_editar_gasto)
        self.main_layout.add_widget(self.main_page)

    def boton_volver_edicion_gasto(self, instance):
        self.main_layout.remove_widget(self.layout_edicion_gasto)
        self.main_layout.add_widget(self.layout_editar_gasto)

    def exit_app(self, instance):
        App.get_running_app().stop()