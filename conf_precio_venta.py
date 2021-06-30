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
import time
from PyQt5.Qt import QPushButton
from ventana_productos import ventana_productos

#Inicio de ventanas
class conf_precio_venta (QDialog): #Puede ser ()QMainWindow, QWidget, QDialog
	def __init__(self, parent=None):
		super(conf_precio_venta, self).__init__(parent)
		loadUi('visual/conf_precio_venta.ui', self) #Abrir archivo UI 

		self.redondeo_vigente()
		self.ganancia_vigente()
		self.tipo_busqueda()

		#Redondeo
		self.si_redondeo.setCheckable(True)
		self.si_redondeo.clicked.connect(self.tipo_busqueda)
		self.no_redondeo.setCheckable(True)
		self.no_redondeo.clicked.connect(self.tipo_busqueda)

		#señal botones
		#Guardar
		self.guardar.clicked.connect(self.guardar_precio_venta)
	
#Funciones de Botones
	#Conciderar si se ajusta con redondeo o no.
	def tipo_busqueda (self):
		if self.si_redondeo.isChecked():
			self.redondeo_vigente()
			self.redondeo.setEnabled(True)
		elif self.no_redondeo.isChecked():
			self.redondeo.setEnabled(False)
			self.redondeo.setText('')
		else:
			self.si_redondeo.setEnabled(True)
			self.no_redondeo.setEnabled(True)

	def ganancia_vigente(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM precio_venta')
		redondeo=cursor.fetchone()
		self.ganancia.setText(redondeo[1])
		
	def redondeo_vigente(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM precio_venta')
		redondeo=cursor.fetchone()
		self.redondeo.setText(redondeo[2])
		self.si_redondeo.setChecked(True)

	def guardar_precio_venta(self):
		ganancia=self.ganancia.text()
		redondeo=self.redondeo.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('UPDATE precio_venta SET ganancia=?,redondeo=? WHERE id=1', (ganancia,redondeo))
		conexion.commit()
		conexion.close()
		


#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = conf_precio_venta()
main.show()
sys.exit(app.exec_())