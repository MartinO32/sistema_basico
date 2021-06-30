import sys
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QButtonGroup, QCompleter, QDialog, QListWidgetItem, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from _sqlite3 import Error, IntegrityError, OperationalError
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtCore import QRegularExpression, pyqtSignal
from PyQt5.QtGui import QIntValidator, QRegularExpressionValidator
import datetime
from datetime import date
from math import ceil
from openpyxl import Workbook
from ventana_directorio import ventana_directorio



class conf_rubros(QMainWindow):
	clicked = pyqtSignal()
	def __init__(self, parent=None):
		super(conf_rubros,self).__init__(parent)
		loadUi('visual/conf_rubros_proveedor.ui', self)

	
	#Configuracion 			
		#Señales
		self.buscador_rubro.returnPressed.connect(self.buscar_existente)
		self.lista_rubros.itemClicked.connect(self.seleccion_rubro)

		#Señales de botones Botones
		self.agregar_rubro.clicked.connect(self.nuevo_rubro)
		self.guardar.clicked.connect(self.guardar_rubro)
		self.modificar.clicked.connect(self.editar_rubro)
		self.eliminar.clicked.connect(self.eliminar_rubro)
		self.limpiar.clicked.connect(self.limpiar_pantalla)

	#Funciones 
	#Busqueda inicial
	def buscar_existente (self):
		self.lista_rubros.clear()
		self.guardar.setEnabled(False)
		buscador=self.buscador_rubro.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM rubro WHERE rubro LIKE ?' ,(f'%{buscador}%',))
		resultado=cursor.fetchall()
		for i in resultado:
			if i[0]=='':
				pass
			else:
				self.lista_rubros.addItem((i[0]))

	def nuevo_rubro (self):
		self.limpiar_pantalla()
		self.guardar.setEnabled(True)
		self.rubro.setEnabled(True)
		self.rubro.setFocus(True)

	def guardar_rubro(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		nuevo=self.rubro.text()
		item=self.lista_rubros.selectedItems()
		if item==[]:
			cursor.execute('INSERT INTO rubro VALUES(?)', [nuevo])
			conexion.commit()
			conexion.close()
			self.limpiar_pantalla()
			QMessageBox.information(self, "Agregado", "Se agregó correctamente un nuevo rubro." , QMessageBox.Ok, QMessageBox.Ok)
		else:
			rubro=item[0].text()
			cursor.execute('UPDATE rubro SET rubro=? WHERE rubro=?',(nuevo, rubro))
			conexion.commit()
			conexion.close()
			self.limpiar_pantalla()
			QMessageBox.information(self, "Modificado", "Se modificó correctamente el rubro." , QMessageBox.Ok, QMessageBox.Ok)

	def seleccion_rubro(self):
		item=self.lista_rubros.selectedItems()
		self.rubro.setText(item[0].text())
		self.guardar.setEnabled(False)
		self.eliminar.setEnabled(True)
		self.modificar.setEnabled(True)
	
	def editar_rubro(self):
		self.rubro.setEnabled(True)
		self.guardar.setEnabled(True)
		self.eliminar.setEnabled(False)
		self.modificar.setEnabled(False)

	def eliminar_rubro(self):
		eliminar=self.rubro.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('DELETE FROM rubro WHERE rubro=?', [eliminar])
		conexion.commit()
		conexion.close()
		self.limpiar_pantalla()
		QMessageBox.information(self, "Borrado", "Se borró correctamente el rubro." , QMessageBox.Ok, QMessageBox.Ok)

	def limpiar_pantalla(self):
		self.buscador_rubro.setText('')
		self.lista_rubros.clear()
		self.rubro.setEnabled(False)
		self.rubro.setText('')
		self.guardar.setEnabled(False)
		self.eliminar.setEnabled(False)
		self.modificar.setEnabled(False)
				
'''
#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = conf_rubros()
main.show()
sys.exit(app.exec_())'''