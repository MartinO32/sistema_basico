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
from ventana_agenda import ventana_agenda

#Inicio de ventanas
class ventana_productos (QDialog): #Puede ser ()QMainWindow, QWidget
	def __init__(self, parent=None):
		super(ventana_productos, self).__init__(parent)
		loadUi('visual/ventana_productos.ui', self) #Abrir archivo UI 

		self.proveedor.setFocus()

	#señales de widgets
		#Proveedor
		autocompletar = QCompleter(self.ver_proveedor())
		autocompletar.setCaseSensitivity(0)
		self.proveedor.setCompleter(autocompletar)
		#Rubro
		autocompletar = QCompleter(self.ver_proveedor())
		autocompletar.setCaseSensitivity(0)
		self.proveedor.setCompleter(autocompletar)
		#Subrubro
		autocompletar = QCompleter(self.ver_proveedor())
		autocompletar.setCaseSensitivity(0)
		self.proveedor.setCompleter(autocompletar)
		

	#Señales botones
		self.nuevo_contacto.clicked.connect(self.agregar_contacto)
		self.btn_precio_venta.clicked.connect(self.insertar_precio_venta)
		self.guardar.clicked.connect(self.guardar_producto)
		self.limpiar.clicked.connect(self.limpiar_pantalla)
	
#Funciones de Botones
	def insertar_precio_venta(self):
		pass
	
	#Lista de proveedores
	def ver_proveedor (self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT nombre FROM proveedor')
		lista=[]
		for i in cursor.fetchall():
			lista.append(i[0])
		conexion.close()
		return lista

	def agregar_contacto(self):
		ventana=ventana_agenda(self)
		ventana.show()

	def guardar_producto (self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		proveedor=self.proveedor.text()
		cursor.execute('SELECT nombre FROM proveedor WHERE nombre=?',[proveedor])
		corroborar_proveedor=cursor.fetchone()
		rubro=self.rubro.text()
		subrubro=self.subrubro.text()
		marca=self.marca.text()
		descripcion=self.descripcion.text()
		codigo=self.codigo.text()
		stock=self.stock.text()
		costo=self.costo.text()
		precio=self.precio_venta.text()
		if self.id_producto.text()=='':
			if proveedor=='' or marca=='' or rubro=='' or subrubro=='' or stock=='' or costo=='' or precio=='':
				QMessageBox.warning(self, 'Error', 'Se encuentran datos incompletos')
			elif proveedor!= corroborar_proveedor[0]:
				self.proveedor.setText('')
				QMessageBox.warning(self, 'Error', 'Debe ingresar un proveedor de la lista')
			else:
				datos=[
					proveedor,
					rubro,
					subrubro,
					marca,
					descripcion,
					codigo,
					stock,
					costo,
					precio
				]
				cursor.execute('INSERT INTO productos VALUES(NULL,?,?,?,?,?,?,?,?,?)',datos)
				conexion.commit()
				QMessageBox.information(self, 'Correcto','Se guardó el nuevo producto correctamente', QMessageBox.Ok, QMessageBox.Ok)
		else:
			if proveedor=='' or marca=='' or rubro=='' or subrubro=='' or stock=='' or costo=='' or precio=='':
				QMessageBox.warning(self, 'Error', 'Se encuentran datos incompletos')
			elif proveedor!= corroborar_proveedor[0]:
				self.proveedor.setText('')
				QMessageBox.warning(self, 'Error', 'Debe ingresar un proveedor de la lista')
			else:
				id=self.id_producto.text()
				datos=[
					proveedor,
					rubro,
					subrubro,
					marca,
					descripcion,
					codigo,
					stock,
					costo,
					precio
				]
				cursor.execute('UPDATE productos SET proveedor=?, rubro=?, subrubro=?, marca=?, descripcion=?, codigo=?, cantidad=?, costo=?, precio_venta=? WHERE id=?', (proveedor,rubro,subrubro,marca,descripcion,codigo,stock,costo,precio,id))
				conexion.commit()
				QMessageBox.information(self, 'Correcto',f'Se modificó\n"{rubro} {subrubro} {marca} {descripcion}"\ncorrectamente', QMessageBox.Ok, QMessageBox.Ok)
		self.limpiar_pantalla()
		conexion.close()

	
	#Limpiar pantalla
	def limpiar_pantalla(self):
		self.id_producto.setText('')
		self.proveedor.setText('')
		self.marca.setText('')
		self.rubro.setText('')
		self.subrubro.setText('')
		self.descripcion.setText('')
		self.codigo.setText('')
		self.stock.setText('')
		self.costo.setText('')
		self.precio_venta.setText('')
		self.guardar.setEnabled(True)
		self.eliminar.setEnabled(False)

'''
#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = ventana_productos()
main.show()
sys.exit(app.exec_())'''