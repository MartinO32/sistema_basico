#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QButtonGroup, QCompleter, QDialog, QListWidgetItem, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from _sqlite3 import Error, IntegrityError, OperationalError
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
import datetime
from datetime import date
from math import ceil
from openpyxl import Workbook
from ventana_compras import ventana_compras
from ventana_agenda import ventana_agenda
from ventana_deposito import ventana_deposito
from conf_precio_venta import conf_precio_venta
from conf_rubros import conf_rubros
from conf_medios import conf_medios
import time
from PyQt5.Qt import QPushButton
import socket


#Inicio de ventanas
class Inicio (QMainWindow): #Puede ser ()QMainWindow, QWidget
	def __init__(self, parent=None):
		super(Inicio, self).__init__(parent)
		loadUi('visual/ventana_inicio.ui', self) #Abrir archivo UI 

		#Usuario activo
		self.muestra_usuario.setText(self.usuario_activo())

	#Fechas
		hoy=QtCore.QDate.currentDate()
		self.fecha.setDate(hoy)

	#Señales botones
		self.cerrar_sesion.clicked.connect(self.salir_sesion)
		self.compras.clicked.connect(self.abrir_compras)
		self.deposito.clicked.connect(self.abrir_deposito)
		self.agenda.clicked.connect(self.abrir_agenda)
	
	#Menu
		self.actionContacto.triggered.connect(self.abrir_agenda)
		self.actionRubros_proveedores.triggered.connect(self.configurar_rubros_proveedores)
		self.actionMedio_de_contacto.triggered.connect(self.configurar_medio_contacto)
		self.actionPrecio_de_venta.triggered.connect(self.configurar_precio_venta)
		
#Funciones de Botones
	def usuario_activo (self):
		terminal=socket.gethostname()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM usuario_activo ORDER by ingreso DESC')
		usuario_activo=cursor.fetchone()
		if usuario_activo[1]==terminal:
			return usuario_activo[0]
		else:
			QMessageBox.warning(self, 'Error', f'El usuario\t"{usuario_activo[0]}"\tes encuentra activo en la PC\t"{usuario_activo[1]}".\n\nCierre el mismo y vuelva a intentarlo')
			self.close()

	def salir_sesion(self):
		salir = QMessageBox.question(self, "Mensaje", "Seguro quiere salir", QMessageBox.Yes, QMessageBox.No)
		if salir == QMessageBox.Yes:
			terminal=socket.gethostname()
			usuario=self.muestra_usuario.text()
			acceso=time.strftime("%d/%m/%y %H:%M:%S")
			conexion=sqlite3.connect('BD.db')
			cursor=conexion.cursor()
			cursor.execute('UPDATE login SET egreso=? WHERE usuario=?',(acceso,usuario))
			conexion.commit()
			cursor.execute('DELETE FROM usuario_activo WHERE usuario=? AND terminal=?',[usuario,terminal])
			conexion.commit()
			conexion.close()
			sys.exit()
		else:
			pass
	
	def abrir_compras(self):
		ventana=ventana_compras(self)
		ventana.show()

	def abrir_deposito(self):
		ventana=ventana_deposito(self)
		ventana.show()

	def abrir_agenda(self):
		ventana=ventana_agenda(self)
		ventana.show()

	def configurar_rubros_proveedores(self):
		ventana=conf_rubros(self)
		ventana.show()

	def configurar_medio_contacto(self):
		ventana=conf_medios(self)
		ventana.show()

	def configurar_precio_venta(self):
		ventana=conf_precio_venta(self)
		ventana.show()


#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = Inicio()
main.show()
sys.exit(app.exec_())