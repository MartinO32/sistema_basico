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
class ventana_deposito (QMainWindow): #Puede ser ()QMainWindow, QWidget
	producto = pyqtSignal(str)
	def __init__(self, parent=None):
		super(ventana_deposito, self).__init__(parent)
		loadUi('visual/ventana_deposito.ui', self) #Abrir archivo UI 

		# Establecer ancho de las columnas
		#Busqueda de productos
		for indice, ancho in enumerate((50,120,120, 150, 120, 150, 70, 70, 80), start=0):
			self.tabla_deposito.setColumnWidth(indice, ancho)

		#busqueda por producto
		self.buscador_producto.returnPressed.connect(self.busqueda_producto)

		#Señales botones
		self.buscar_producto.clicked.connect(self.busqueda_producto)
		self.nuevo_producto.clicked.connect(self.agregar_producto)
		self.modificar_producto.clicked.connect(self.editar_producto)
				
		#Foco en el buscador de producto
		self.buscador_producto.setFocus()

#Funciones de Botones
	#Busqueda productos
	def busqueda_producto (self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		dato=self.buscador_producto.text()
		cursor.execute("SELECT * FROM productos WHERE proveedor LIKE ? or id LIKE ? OR rubro LIKE ? OR subrubro LIKE ? OR marca LIKE ? OR descripcion LIKE ? OR codigo LIKE ?",(f'%{dato}%', f'%{dato}%', f'%{dato}%',f'%{dato}%',f'%{dato}%',f'%{dato}%',f'%{dato}%',))
		datos=cursor.fetchall()
		if datos==[]:
			filas=self.tabla_deposito.rowCount()
			for i in range(filas):
				self.tabla_deposito.removeRow(0)
			QMessageBox.information(self, 'Error','No hay producto/artículo para está busqueda', QMessageBox.Ok, QMessageBox.Ok)
		else:
			filas=self.tabla_deposito.rowCount()
			for i in range(filas):
				self.tabla_deposito.removeRow(0)
			for i in datos:
				self.tabla_deposito.clearContents()
			n=0
			for i in datos:
				self.tabla_deposito.setRowCount(n + 1)
				self.tabla_deposito.setItem(n, 0, QTableWidgetItem(str(i[0])))
				self.tabla_deposito.setItem(n, 1, QTableWidgetItem(i[1]))
				self.tabla_deposito.setItem(n, 2, QTableWidgetItem(i[2]))
				self.tabla_deposito.setItem(n, 3, QTableWidgetItem(i[3]))
				self.tabla_deposito.setItem(n, 4, QTableWidgetItem(i[4]))
				self.tabla_deposito.setItem(n, 5, QTableWidgetItem(i[5]))
				self.tabla_deposito.setItem(n, 6, QTableWidgetItem(str(i[6])))
				self.tabla_deposito.setItem(n, 7, QTableWidgetItem(str(i[7])))
				self.tabla_deposito.setItem(n, 8, QTableWidgetItem(str(i[8])))
				self.tabla_deposito.setItem(n, 9, QTableWidgetItem(str(i[9])))
				n+=1
		self.buscador_producto.setFocus()

	def agregar_producto(self):
		ventana=ventana_productos(self)
		ventana.show()

	def editar_producto(self):
		seleccion=self.tabla_deposito.selectedItems()	
		if seleccion == [] :
			QMessageBox.warning(self, 'Error', 'No se ha seleccionado ningún comprobante para anular')
		else:	
			ventana=ventana_productos(self)
			ventana.guardar.setEnabled(True)
			ventana.eliminar.setEnabled(True)
			ventana.id_producto.setText(seleccion[0].text())
			ventana.proveedor.setText(seleccion[1].text())
			ventana.rubro.setText(seleccion[2].text())
			ventana.subrubro.setText(seleccion[3].text())
			ventana.marca.setText(seleccion[4].text())
			ventana.descripcion.setText(seleccion[5].text())
			ventana.codigo.setText(seleccion[6].text())
			ventana.stock.setText(seleccion[7].text())
			ventana.costo.setText(seleccion[8].text())
			ventana.precio_venta.setText(seleccion[9].text())
			ventana.show()

	def productos_fallados (self):pass	

#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = ventana_deposito()
main.show()
sys.exit(app.exec_())