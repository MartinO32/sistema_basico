import sys
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QButtonGroup, QCompleter, QDialog, QListWidgetItem, QMainWindow, QMessageBox, QTableWidgetItem
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
from ventana_factura_compra import ventana_factura_compra
from ventana_facturas_anuladas import ventana_facturas_anuladas


class ventana_compras(QMainWindow):
	
	def __init__(self, parent=None):
		super(ventana_compras,self).__init__(parent)
		loadUi('visual/ventana_compras.ui', self)

		self.carga_facturas.clicked.connect(self.abrir_carga_facturas)
		self.facturas_anuladas.clicked.connect(self.abrir_facturas_anuladas)

#Funciones de Botones
	def abrir_carga_facturas(self):
		ventana=ventana_factura_compra(self)
		ventana.show()

	
	def abrir_facturas_anuladas(self):
		ventana=ventana_facturas_anuladas(self)
		ventana.show()
'''
#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = ventana_compras()
main.show()
sys.exit(app.exec_())'''