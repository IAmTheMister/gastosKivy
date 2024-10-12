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

class Calculos:
    def calcular_gasto_dia(self, usuario, dia):
        gasto_total = 0
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row and row[0] == dia:
                    gasto_total += round(float(row[3]), 2)
        return gasto_total

    def calcular_gasto_ing_intervalo(self, fin, inicio, usuario):
        gasto_total = 0
        with open(usuario + "/gastos" + "_" + usuario + ".csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
                fecha_fin = datetime.strptime(fin, "%d/%m/%Y")
                if row and fecha_inicio <= fecha_row <= fecha_fin:
                    if row[4] == "Ingresos":
                        gasto_total += round(float(row[3]), 2)
        return gasto_total

    def calcular_gasto_ahorros_intervalo(self, fin, inicio, usuario):
        gasto_total = 0
        with open(usuario + "/gastos" + "_" + usuario + ".csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
                fecha_fin = datetime.strptime(fin, "%d/%m/%Y")
                if row and fecha_inicio <= fecha_row <= fecha_fin:
                    if row[4] == "Ahorros":
                        gasto_total += round(float(row[3]), 2)
        return gasto_total

    def calcular_saldo_intervalo(self, fin, inicio, usuario):
        gasto_total = 0
        ingresos = 0
        with open(usuario + "/ingresos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
                fecha_fin = datetime.strptime(fin, "%d/%m/%Y")
                if row and fecha_inicio <= fecha_row <= fecha_fin:
                    ingresos += round(float(row[1]), 2)
        with open(usuario + "/gastos" + "_" + usuario + ".csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
                fecha_fin = datetime.strptime(fin, "%d/%m/%Y")
                if row and fecha_inicio <= fecha_row <= fecha_fin:
                    gasto_total += round(float(row[3]), 2)
        return gasto_total, ingresos

    def calcular_gasto_ing_mes(self,usuario, ano, mes):
        gasto_total = 0
        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if row and fecha_row.year == ano and fecha_row.month == mes:
                    if row[4] == "Ingresos":
                        gasto_total += round(float(row[3]), 2)

        return gasto_total

    def calcular_gasto_ahorros_mes(self,usuario, ano, mes):
        gasto_total = 0
        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if row and fecha_row.year == ano and fecha_row.month == mes:
                    if row[4] == "Ahorros":
                        gasto_total += round(float(row[3]), 2)

        return gasto_total

    def calcular_saldo_mes(self,usuario, ano, mes):
        gasto_total = 0
        ingresos = 0
        with open(usuario + "/ingresos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if row and fecha_row.year == ano and fecha_row.month == mes:
                    ingresos += round(float(row[1]), 2)
        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if row and fecha_row.year == ano and fecha_row.month == mes:
                    gasto_total += round(float(row[3]), 2)

        return gasto_total, ingresos

    def calcular_alquiler_mes(self,usuario,ano, mes):
        alquiler_mes = 0
        with open(usuario + "/gastos"+"_"+usuario+".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                cat = row[2]
                if row and fecha_row.year == ano and fecha_row.month == mes and cat == "Alquiler":
                    alquiler_mes += round(float(row[3]), 2)
        return alquiler_mes

    def calcular_saldo_ano(self, ano, usuario):
        gasto_total = 0
        ingresos = 0
        with open(usuario + "/ingresos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if row and fecha_row.year == ano:
                    ingresos += round(float(row[1]), 2)
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                if row and fecha_row.year == ano:
                    gasto_total += round(float(row[3]), 2)
        return gasto_total, ingresos

    def calcular_alquiler_ano(self, ano, usuario):
        alquiler = 0
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                fecha_row = datetime.strptime(row[0], "%d/%m/%Y")
                cat = row[2]
                if row and fecha_row.year == ano and cat == "Alquiler":
                    alquiler += round(float(row[3]), 2)
        return alquiler

    def calcular_saldo_total(self, usuario):
        gasto_total = 0
        ingresos = 0
        with open(usuario + "/ingresos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row:
                    ingresos += round(float(row[1]), 2)
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row:
                    gasto_total += round(float(row[3]), 2)
        return gasto_total, ingresos

    def calcular_alquiler_total(self, usuario):
        alquiler = 0
        with open(usuario + "/gastos" + "_" + usuario + ".csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                cat = row[2]
                if row and cat == "Alquiler":
                    alquiler += round(float(row[3]), 2)
        return alquiler