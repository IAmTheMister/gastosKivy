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
from hashlib import sha256

class Perfil:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page
        self.altura = 0.21
        
    def menu_perfil(self,usuario):
        self.layout_perfil = GridLayout(cols=1, spacing=10, height = Window.height)
        self.layout_navegacion_perfil = GridLayout(cols=2, height=Window.height * 0.05, size_hint_y=None)
        btn_exit = Button(text='Salir', on_press=partial(self.exit_app), height=Window.height * 0.05, size_hint_y=None,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        btn_volver = Button(text='Volver', on_press=partial(self.boton_volver_perfil), height=Window.height * 0.05,
                            size_hint_y=None,
                            background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_perfil.add_widget(btn_exit)
        self.layout_navegacion_perfil.add_widget(btn_volver)
        self.layout_perfil.add_widget(self.layout_navegacion_perfil)

        self.usuario_nuevo = TextInput(hint_text = "Usuario nuevo",height=Window.height * 0.05,size_hint_y=None)
        self.contrasena_nueva = TextInput(hint_text="Contraseña nueva", height=Window.height * 0.05, size_hint_y=None,
                                          password = True)
        btn_cambiar_usuario = Button(text = "Cambiar usuario", on_press = partial(self.cambiar_usuario, usuario),
                                     height=Window.height * 0.05,size_hint_y=None)
        btn_cambiar_contraseña = Button(text="Cambiar contraseña", on_press = partial(self.cambiar_contrasena, usuario),
                                        height=Window.height * 0.05, size_hint_y=None)

        self.layout_perfil.add_widget(self.usuario_nuevo)
        self.layout_perfil.add_widget(btn_cambiar_usuario)
        self.layout_perfil.add_widget(self.contrasena_nueva)
        self.layout_perfil.add_widget(btn_cambiar_contraseña)

        self.main_layout.add_widget(self.layout_perfil)

    def cambiar_usuario(self, usuario, instance):
        usuario_nuevo = self.usuario_nuevo.text
        lista_usuarios = self.fetch_datos_usuarios()
        for i in range(len(lista_usuarios)):
            if usuario == lista_usuarios[i][0]:
                lista_usuarios[i][0] = usuario_nuevo

        with open("usuarios.csv", newline='\n', mode= "w") as csvfile:
            write = csv.writer(csvfile, delimiter=",")
            for i in range(len(lista_usuarios)):
                write.writerow([lista_usuarios[i][0], lista_usuarios[i][1]])

    def cambiar_contrasena(self, usuario, instance):
        contrasena_nueva = self.contrasena_nueva.text
        lista_usuarios = self.fetch_datos_usuarios()
        for i in range(len(lista_usuarios)):
            if usuario == lista_usuarios[i][0]:
                lista_usuarios[i][1] = self.hash(contrasena_nueva)

        with open("usuarios.csv", newline='\n', mode= "w") as csvfile:
            write = csv.writer(csvfile, delimiter=",")
            for i in range(len(lista_usuarios)):
                write.writerow([lista_usuarios[i][0], lista_usuarios[i][1]])

    def fetch_datos_usuarios(self):
        lista_usuarios = []
        with open("usuarios.csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lista_usuarios.append([row[0], row[1]])
        return lista_usuarios
        
    def boton_volver_perfil(self, instance):
        self.main_layout.remove_widget(self.layout_perfil)
        self.main_layout.add_widget(self.main_page)

    def exit_app(self, instance):
        App.get_running_app().stop()

    def hash(self, input):
        return sha256(input.encode('utf-8')).hexdigest()