import sys
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QButtonGroup, QCompleter, QDialog, QListWidgetItem, QMainWindow, QMessageBox, QTableWidgetItem, QVBoxLayout
from PyQt5.uic import loadUi
from _sqlite3 import Error, IntegrityError, OperationalError
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator
import datetime
from datetime import date
from math import ceil
from openpyxl import Workbook
from PyQt5.QtCore import pyqtSignal
#from ventana_factura_compra import ventana_factura_compra

class ventana_buscar_factura_compra(QMainWindow):
	datos_factura = pyqtSignal(str)
	def __init__(self, parent=None):
		super(ventana_buscar_factura_compra,self).__init__(parent)
		loadUi('visual/buscar_facturas.ui', self)

	#busqueda de facturas
		self.busqueda_factura.returnPressed.connect(self.busqueda_facturas)

	# Establecer ancho de las columnas
		#Busqueda de productos
		for indice, ancho in enumerate((50, 150, 150, 100), start=0):
			self.tabla_busqueda_facturas.setColumnWidth(indice, ancho)

	#señal de boton
		self.mostrar.clicked.connect(self.mostrar_detalle)
		
#Funciones de Botones
	#Busqueda productos
	def busqueda_facturas(self):
		self.limpiar_filas()
		self.tabla_busqueda_facturas.clearContents()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		dato=self.busqueda_factura.text()
		lista=[]
		cursor.execute("SELECT * FROM facturas_compra WHERE id LIKE ? OR proveedor LIKE ? OR numero LIKE ? OR total LIKE ?",(f'%{dato}%',f'%{dato}%',f'%{dato}%',f'%{dato}%',))
		datos=cursor.fetchall()
		for i in datos:
			self.tabla_busqueda_facturas.clearContents()
		n=0
		for i in datos:
			self.tabla_busqueda_facturas.setRowCount(n + 1)
			self.tabla_busqueda_facturas.setItem(n, 0, QTableWidgetItem(str(i[0])))
			self.tabla_busqueda_facturas.setItem(n, 1, QTableWidgetItem(i[1]))
			self.tabla_busqueda_facturas.setItem(n, 2, QTableWidgetItem(i[3]))
			self.tabla_busqueda_facturas.setItem(n, 3, QTableWidgetItem(i[10]))
			n+=1

	#Abrir factura seleccionada
	def mostrar_detalle(self):
		seleccion=self.tabla_busqueda_facturas.selectedItems()
		if seleccion!=[]:
			datos=[seleccion[0].text()]
			
			#Enviar datos a pantalla de factura
			self.datos_factura.emit(datos[0])
			#Cerrar ventana
			self.close()
		else:
			QMessageBox.warning(self, 'Error', 'No se ha seleccionado ningún comprobante')

	#Eliminar filas de tabla facturas
	def limpiar_filas(self):
		self.tabla_busqueda_facturas.clearContents()	
		filas=self.tabla_busqueda_facturas.rowCount()
		for i in range(filas):
			self.tabla_busqueda_facturas.removeRow(0)

'''
#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = ventana_buscar_factura_compra()
main.show()
sys.exit(app.exec_())'''