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



class conf_medios(QMainWindow):
	clicked = pyqtSignal()
	def __init__(self, parent=None):
		super(conf_medios,self).__init__(parent)
		loadUi('visual/conf_medios_contacto.ui', self)

	#Configuracion 			
		#Señales
		self.buscador_medio.returnPressed.connect(self.buscar_existente)
		self.lista_medios.itemClicked.connect(self.seleccion_medio)

		#Señales de botones Botones
		self.agregar_medio.clicked.connect(self.nuevo_medio)
		self.guardar.clicked.connect(self.guardar_medio)
		self.modificar.clicked.connect(self.editar_medio)
		self.eliminar.clicked.connect(self.eliminar_medio)
		self.limpiar.clicked.connect(self.limpiar_pantalla)

	#Funciones 
	#Busqueda inicial
	def buscar_existente (self):
		self.lista_medios.clear()
		self.guardar.setEnabled(False)
		buscador=self.buscador_medio.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM medio_contacto WHERE medio LIKE ?' ,(f'%{buscador}%',))
		resultado=cursor.fetchall()
		for i in resultado:
			if i[0]=='':
				pass
			else:
				self.lista_medios.addItem((i[0]))

	def nuevo_medio (self):
		self.limpiar_pantalla()
		self.guardar.setEnabled(True)
		self.medio_contacto.setEnabled(True)
		self.medio_contacto.setFocus(True)

	def guardar_medio(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		nuevo=self.medio_contacto.text()
		item=self.lista_medios.selectedItems()
		if item==[]:
			cursor.execute('INSERT INTO medio_contacto VALUES(?)', [nuevo])
			conexion.commit()
			conexion.close()
			self.limpiar_pantalla()
			QMessageBox.information(self, "Agregado", "Se agregó correctamente un nuevo medio de contacto." , QMessageBox.Ok, QMessageBox.Ok)
		else:
			medio=item[0].text()
			cursor.execute('UPDATE medio_contacto SET medio=? WHERE medio=?',(nuevo, medio))
			conexion.commit()
			conexion.close()
			self.limpiar_pantalla()
			QMessageBox.information(self, "Modificado", "Se modificó correctamente el medio de contacto." , QMessageBox.Ok, QMessageBox.Ok)
			
	def seleccion_medio(self):
		item=self.lista_medios.selectedItems()
		self.medio_contacto.setText(item[0].text())
		self.guardar.setEnabled(False)
		self.eliminar.setEnabled(True)
		self.modificar.setEnabled(True)
	
	def editar_medio(self):
		self.medio_contacto.setEnabled(True)
		self.guardar.setEnabled(True)
		self.eliminar.setEnabled(False)
		self.modificar.setEnabled(False)

	def eliminar_medio(self):
		eliminar=self.medio_contacto.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('DELETE FROM medio_contacto WHERE medio=?', [eliminar])
		conexion.commit()
		conexion.close()
		self.limpiar_pantalla()
		QMessageBox.information(self, "Borrado", "Se borró correctamente el medio de contacto." , QMessageBox.Ok, QMessageBox.Ok)

	def limpiar_pantalla(self):
		self.buscador_medio.setText('')
		self.lista_medios.clear()
		self.medio_contacto.setEnabled(False)
		self.medio_contacto.setText('')
		self.guardar.setEnabled(False)
		self.eliminar.setEnabled(False)
		self.modificar.setEnabled(False)
				
'''
#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = conf_medios()
main.show()
sys.exit(app.exec_())'''