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
from kivy.uix.popup import Popup
import csv
import json
from datetime import datetime
from hashlib import sha256
from functools import partial
import os

from dia import Dia
from intervalo import Intervalo
from mes import Mes
from ano import Ano
from anadirgasto import AnadirGasto
from anadiringreso import AnadirIngreso
from editargasto import EditarGasto
from editaringreso import EditarIngreso
from totales import ClaseTotal
from buscar_concepto import BuscarConcepto
from perfil import Perfil
from viajes import Viajes

class MiApp(App):
    def build(self):
        Window.size = (600,600)
        # Crea una caja vertical (BoxLayout)
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        with self.main_layout.canvas.before:
            Color(0.35, 0.65, 0.35, 0.6)  # RGBA (valores entre 0 y 1)
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self.update_rect)
        self.menu_inicio()
        return self.main_layout

    def menu_inicio(self):
        self.layout_inicio = GridLayout(cols = 1, spacing = 10)

        self.usuario = TextInput(hint_text = "Usuario", height=Window.height * 0.05,size_hint_y=None)
        self.contrasena = TextInput(hint_text = "Contraseña", height=Window.height * 0.05,size_hint_y=None,
                                    password = True)
        self.layout_inicio.add_widget(self.usuario)
        self.layout_inicio.add_widget(self.contrasena)

        btn_login = Button(text = "Iniciar sesión", on_press = partial(self.login),
                           height=Window.height * 0.05,size_hint_y=None)

        self.layout_inicio.add_widget(btn_login)

        btn_register = Button(text="Registrarse", on_press=partial(self.menu_registro),
                              height=Window.height * 0.05, size_hint_y=None)

        self.layout_inicio.add_widget(btn_register)

        self.main_layout.add_widget(self.layout_inicio)

    def login(self, instance):
        with open("usuarios.csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if self.usuario.text == row[0] and self.hash(self.contrasena.text) == row[1]:
                    self.main_layout.remove_widget(self.layout_inicio)
                    self.menu_principal(self.usuario.text)

    def menu_registro(self, instance):
        self.main_layout.remove_widget(self.layout_inicio)
        self.layout_register = GridLayout(cols = 1, spacing = 10)
        label_register = Label(text = "Formulario de registro", height=Window.height * 0.05, size_hint_y=None)
        self.layout_register.add_widget(label_register)
        self.usuario_register = TextInput(hint_text="Usuario", height=Window.height * 0.05, size_hint_y=None)
        self.contrasena_register = TextInput(hint_text="Contraseña", height=Window.height * 0.05, size_hint_y=None,
                                    password=True)
        self.contrasena_register_conf = TextInput(hint_text="Repita contraseña", height=Window.height * 0.05, size_hint_y=None,
                                    password=True)
        self.layout_register.add_widget(self.usuario_register)
        self.layout_register.add_widget(self.contrasena_register)
        self.layout_register.add_widget(self.contrasena_register_conf)

        btn_register = Button(text="Registrarse", on_press=partial(self.register),
                              height=Window.height * 0.05, size_hint_y=None)

        self.layout_register.add_widget(btn_register)

        self.main_layout.add_widget(self.layout_register)

    def register(self, instance):
        self.layout_popup_error = GridLayout(cols = 1, spacing = 5)
        if self.contrasena_register.text != self.contrasena_register_conf.text:
            msj = Popup(title = "Error" , content=self.layout_popup_error,
                      size_hint=(None, None), size=(Window.width * 0.5, Window.height * 0.25))
            error_contrasena = Label(text="Las contraseñas no \n coinciden")
            self.layout_popup_error.add_widget(error_contrasena)
            btn_cerrar_popup = Button(text="Cerrar", size=(Window.width * 0.5, Window.height * 0.05),
                                      on_press=msj.dismiss)
            self.layout_popup_error.add_widget(btn_cerrar_popup)
            msj.open()
        else:
            with open("usuarios.csv", mode='a', newline="\n") as csvfile:
                write = csv.writer(csvfile, delimiter=",")
                write.writerow([self.usuario_register.text, self.hash(self.contrasena_register.text)])
            os.makedirs(self.usuario_register.text)
            with open(self.usuario_register.text + "/ingresos"+"_"+self.usuario_register.text+".csv",
                      mode='x', newline="\n") as csvfile:
                pass
            with open(self.usuario_register.text + "/gastos" + "_" + self.usuario_register.text + ".csv",
                      mode='x',newline="\n") as csv_file:
                pass

    def hash(self, input):
        return sha256(input.encode('utf-8')).hexdigest()

    def menu_principal(self,usuario):
        self.main_page = GridLayout(cols=1, spacing=10)
        self.layout_menu = GridLayout(cols=2, spacing=10)
        self.layout_navegacion_menu = GridLayout(cols=2, spacing=5, height=Window.height * 0.1, size_hint_y=None)
        btn_anadir_gasto = Button(text='Añadir gasto', on_press=partial(self.pagina_anadir_gasto,usuario), height=Window.height * 0.1,
                                  size_hint_y=None)
        btn_anadir_ingreso = Button(text='Añadir ingreso', height=Window.height * 0.1,on_press=partial(self.pagina_anadir_ingreso,usuario),
                                  size_hint_y=None)
        btn_dia = Button(text='Estadisticas por dia', on_press= partial(self.pagina_dia,usuario), height = Window.height*0.1,
                         size_hint_y =None)
        btn_intervalo = Button(text='Estadisticas por intervalo', on_press = partial(self.pagina_intervalo,usuario), height = Window.height*0.1,
                               size_hint_y =None)
        btn_mes = Button(text='Estadisticas por mes', on_press = partial(self.pagina_mes,usuario), height=Window.height * 0.1,
                         size_hint_y=None)
        btn_ano = Button(text='Estadisticas por año', on_press = partial(self.pagina_ano,usuario), height = Window.height*0.1,
                         size_hint_y =None)
        btn_editar_gasto = Button(text='Editar gasto', on_press = partial(self.pagina_editar_gasto,usuario), height=Window.height * 0.1,
                                  size_hint_y=None)
        btn_editar_ingreso = Button(text='Editar ingreso', on_press = partial(self.pagina_editar_ingreso,usuario), height=Window.height * 0.1,
                                    size_hint_y=None)
        btn_total = Button(text='Estadisticas totales', on_press=partial(self.pagina_total, usuario), height=Window.height * 0.1,
                         size_hint_y=None)

        btn_buscar_concepto = Button(text='Buscar por concepto', on_press=partial(self.pagina_buscar_concepto, usuario),
                           height=Window.height * 0.1,
                           size_hint_y=None)

        btn_viajes = Button(text='Viajes', on_press=partial(self.pagina_viajes, usuario),
                                     height=Window.height * 0.1,
                                     size_hint_y=None)

        btn_exit = Button(text='Salir', on_press=self.exit_app,height=Window.height * 0.1, size_hint_y=None,
                               background_color=(2,2,2,1), color = (0,0,0,1))

        btn_perfil= Button(text='Perfil', on_press = partial(self.pagina_perfil, usuario),
                           height=Window.height * 0.1, size_hint_y=None, size_hint_x = 0.2,
                          background_color=(2, 2, 2, 1), color=(0, 0, 0, 1))

        self.layout_navegacion_menu.add_widget(btn_exit)
        self.layout_navegacion_menu.add_widget(btn_perfil)
        self.main_page.add_widget(self.layout_navegacion_menu)

        self.layout_menu.add_widget(btn_anadir_gasto)
        self.layout_menu.add_widget(btn_anadir_ingreso)
        self.layout_menu.add_widget(btn_editar_gasto)
        self.layout_menu.add_widget(btn_editar_ingreso)
        self.layout_menu.add_widget(btn_dia)
        self.layout_menu.add_widget(btn_intervalo)
        self.layout_menu.add_widget(btn_mes)
        self.layout_menu.add_widget(btn_ano)
        self.layout_menu.add_widget(btn_total)
        self.layout_menu.add_widget(btn_buscar_concepto)
        self.layout_menu.add_widget(btn_viajes)
        self.main_page.add_widget(self.layout_menu)
        self.main_layout.add_widget(self.main_page)

    def pagina_dia(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_dia = Dia(self.main_layout, self.main_page)
        clase_dia.menu_dia(usuario)

    def pagina_intervalo(self,usuario,instance):
        self.main_layout.remove_widget(self.main_page)
        clase_intervalo = Intervalo(self.main_layout, self.main_page)
        clase_intervalo.menu_intervalo(usuario)

    def pagina_mes(self,usuario,instance):
        self.main_layout.remove_widget(self.main_page)
        clase_mes = Mes(self.main_layout, self.main_page)
        clase_mes.menu_mes(usuario)

    def pagina_ano(self,usuario,instance):
        self.main_layout.remove_widget(self.main_page)
        clase_ano = Ano(self.main_layout, self.main_page)
        clase_ano.menu_ano(usuario)

    def pagina_anadir_gasto(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_anadir_gasto = AnadirGasto(self.main_layout, self.main_page)
        clase_anadir_gasto.menu_anadir_gasto(usuario)

    def pagina_anadir_ingreso(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_anadir_ingreso = AnadirIngreso(self.main_layout, self.main_page)
        clase_anadir_ingreso.menu_anadir_ingreso(usuario)

    def pagina_editar_gasto(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_editar_gasto = EditarGasto(self.main_layout, self.main_page)
        clase_editar_gasto.menu_editar_gasto(usuario)

    def pagina_editar_ingreso(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_editar_ingreso = EditarIngreso(self.main_layout, self.main_page)
        clase_editar_ingreso.menu_editar_ingreso(usuario)

    def pagina_total(self,usuario,instance):
        self.main_layout.remove_widget(self.main_page)
        clase_total = ClaseTotal(self.main_layout, self.main_page)
        clase_total.menu_total(usuario)

    def pagina_buscar_concepto(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_buscar_concepto = BuscarConcepto(self.main_layout, self.main_page)
        clase_buscar_concepto.menu_concepto(usuario)

    def pagina_viajes(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_viajes = Viajes(self.main_layout, self.main_page)
        clase_viajes.menu_viajes(usuario)

    def pagina_perfil(self,usuario, instance):
        self.main_layout.remove_widget(self.main_page)
        clase_perfil = Perfil(self.main_layout, self.main_page)
        clase_perfil.menu_perfil(usuario)

    def exit_app(self, instance):
        App.get_running_app().stop()

    def update_rect(self, instance, value):
        # Actualiza el tamaño y la posición del Rectangle al cambiar el tamaño de la ventana
        self.rect.size = instance.size
        self.rect.pos = instance.pos

if __name__ == '__main__':
    MiApp().run()