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
from conf_rubros import conf_rubros
from conf_medios import conf_medios


class ventana_agenda(QMainWindow):
	clicked = pyqtSignal()
	def __init__(self, parent=None):
		super(ventana_agenda,self).__init__(parent)
		loadUi('visual/agenda.ui', self)
		self.limpiar_pantalla()
	#Listas
		#Contactos
		tipo_contacto=[' ','Cliente', 'Proveedor']
		self.tipo_contacto.addItems(tipo_contacto)
				
		#Sexo
		self.sexo.addItems(self.lista_sexo())
				
		#Ivas
		self.tipo_iva.addItems(self.lista_ivas())

		#Tipos de documentos
		self.seleccion_iva()
	
		# Establecer ancho de las columnas
		#Tabla de contactos
		for indice, ancho in enumerate((180, 142, 90), start=0):
			self.tabla_contactos.setColumnWidth(indice, ancho)

	#Configuracion 			
		#Señales
		self.buscador.returnPressed.connect(self.buscar_existente)
		self.tabla_contactos.itemClicked.connect(self.recuperar_datos)
		self.tipo_iva.currentIndexChanged.connect(self.seleccion_iva)
		self.tipo_doc.currentIndexChanged.connect(self.conf_numero)
		
		#Señales de botones Botones
		self.tipo_contacto.textActivated.connect(self.conf_contacto)
		self.agenda_completa.clicked.connect(self.abrir_directorio)
		self.nuevo_contacto.clicked.connect(self.nuevo)
		self.nuevo_medio.clicked.connect(self.agregar_medio)
		self.nuevo_rubro.clicked.connect(self.agregar_rubro)
		self.guardar.clicked.connect(self.guardar_contacto)
		self.modificar.clicked.connect(self.editar_contacto)
		self.eliminar.clicked.connect(self.eliminar_contacto)
		self.limpiar.clicked.connect(self.limpiar_pantalla)

#Funciones de Botones
	#Busqueda inicial
	def buscar_existente (self):
		self.grupo_contacto.setEnabled(False)
		self.guardar.setEnabled(False)
		buscador=self.buscador.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute("""SELECT apellido, nombre, numero, tipo FROM cliente 
				WHERE nombre LIKE ? or apellido LIKE ? or numero LIKE ?
				UNION ALL SELECT NULL as apellido, nombre, numero, tipo FROM proveedor
				WHERE nombre LIKE ? or numero LIKE ? """,
				(f'%{buscador}%',f'%{buscador}%',f'%{buscador}%',f'%{buscador}%',f'%{buscador}%'))
		resultado=cursor.fetchall()
		n=0
		for i in resultado:
			if i[0]!=None:
				self.tabla_contactos.setRowCount(n + 1)
				self.tabla_contactos.setItem(n, 0, QTableWidgetItem(((i[0])+', '+(i[1]))))
				self.tabla_contactos.setItem(n, 1, QTableWidgetItem(i[2]))
				self.tabla_contactos.setItem(n, 2, QTableWidgetItem(i[3]))
				n+=1
			else:
				self.tabla_contactos.setRowCount(n + 1)
				self.tabla_contactos.setItem(n, 0, QTableWidgetItem(i[1]))
				self.tabla_contactos.setItem(n, 1, QTableWidgetItem(i[2]))
				self.tabla_contactos.setItem(n, 2, QTableWidgetItem(i[3]))
				n+=1
		conexion.close()	

	#Datos de Busqueda
	def recuperar_datos(self):
		self.grupo_contacto.setEnabled(False)
		self.guardar.setEnabled(False)
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		#selecion de la tabla
		seleccion=self.tabla_contactos.selectedItems()
		#Lo segun tipo de cliente es si dividimos el nombre o no
		self.tipo_contacto.setCurrentText(seleccion[2].text())
		self.eliminar.setEnabled(True)
		self.modificar.setEnabled(True)		
		if seleccion[2].text()=='Cliente':
			nombre=(seleccion[0].text()).split(sep=', ')
			self.apellido.setText(nombre[0])
			self.nombre.setText(nombre[1])
			numero=seleccion[1].text()
			cursor.execute("SELECT * FROM cliente WHERE numero=?",[numero])
			resultado=cursor.fetchone()
			self.tipo_iva.setCurrentText(resultado[2])
			self.tipo_doc.setCurrentText(resultado[5])
			self.numero.setText(numero)
			self.sexo.setCurrentText(resultado[7])
			self.direccion.setText(resultado[8])
			self.localidad.setText(resultado[9])
			self.telefono.setText(resultado[10])
			self.email.setText(resultado[11])
			self.medio_contacto.setCurrentText(resultado[12])
			self.rubro.setCurrentText('')
		else:
			nombre=[seleccion[0].text()]
			self.apellido.setText(' ')
			self.nombre.setText(nombre[0])
			numero=seleccion[1].text()
			cursor.execute("SELECT * FROM proveedor WHERE numero=?",[numero])
			resultado=cursor.fetchone()
			self.tipo_iva.setCurrentText(resultado[2])
			self.tipo_doc.setCurrentText(resultado[3])
			self.numero.setText(numero)
			self.direccion.setText(resultado[5])
			self.localidad.setText(resultado[6])
			self.telefono.setText(resultado[7])
			self.email.setText(resultado[8])
			self.rubro.setCurrentText(resultado[10])
			self.sexo.setCurrentText('')
			self.medio_contacto.setCurrentText('')
		conexion.close()

	def seleccion_iva (self):
		tipo_iva=self.tipo_iva.currentText()
		if tipo_iva=='Consumidor Final':
			doc=[
			'CUIT',
			'CDI',
			'DNI',
			'Pasaporte',
			'CI Extranjera']
			self.tipo_doc.clear()
			self.tipo_doc.addItems(doc)
		elif tipo_iva=='Proveedor del Exterior' or tipo_iva=='Cliente del Exterior':
			doc=[
			'Pasaporte',
			'CI Extranjera',
			'Otro'	]
			self.tipo_doc.clear()
			self.tipo_doc.addItems(doc)
		elif tipo_iva=='':
			doc=[
			'',
			'CUIT',
			'CDI',
			'DNI',
			'Pasaporte',
			'CI Extranjera',
			'Otro']
			self.tipo_doc.clear()
			self.tipo_doc.addItems(doc)
		else:
			doc=['CUIT']
			self.tipo_doc.clear()
			self.tipo_doc.addItems(doc)

	#Número segun tipo de documento
	def conf_numero(self):
		tipo_doc=self.tipo_doc.currentText()
		if tipo_doc=='DNI':
			self.numero.setMaxLength(8)
			conf = QRegularExpressionValidator(self)
			conf.setRegularExpression(QRegularExpression("(^[1-9][0-9]*(:[1-9][0-9]*)?$)?"))
			self.numero.setValidator(conf)
		elif tipo_doc=='CDI' or tipo_doc=='CUIT' or tipo_doc=='CUIL' :
			self.numero.setMaxLength(11)
			conf = QRegularExpressionValidator(self)
			conf.setRegularExpression(QRegularExpression("(^[1-9][0-9]*(:[1-9][0-9]*)?$)?"))
			self.numero.setValidator(conf)
		else:
			self.numero.setMaxLength(15)
			conf = QRegularExpressionValidator(self)
			conf.setRegularExpression(QRegularExpression("(^[1-9a-zA-Z][0-9a-zA-Z]*(:[1-9a-zA-Z][0-9a-zA-Z]*)?$)?"))
			self.numero.setValidator(conf)

	def nuevo (self):
		self.limpiar_pantalla()
		self.lista_medios()
		self.lista_rubro()
		self.nuevo_contacto.setEnabled(False)
		self.guardar.setEnabled(True)
		self.grupo_contacto.setEnabled(True)
		self.tipo_contacto.setEnabled(True)
		self.tipo_iva.setEnabled(True)
		self.tipo_doc.setEnabled(True)
		self.numero.setEnabled(True)
		self.sexo.setEnabled(True)
		self.direccion.setEnabled(True)
		self.localidad.setEnabled(True)
		self.telefono.setEnabled(True)
		self.email.setEnabled(True)
		self.conf_contacto()
	
	#Configuración si es cliente o proveedor
	def conf_contacto(self):
		if self.tipo_contacto.currentText() == 'Cliente':
			self.grupo_medio.setEnabled(True)
			self.grupo_rubro.setEnabled(False)
			self.sexo.setEnabled(True)
			self.apellido.setEnabled(True)
		elif self.tipo_contacto.currentText() == 'Proveedor':
			self.grupo_rubro.setEnabled(True)
			self.grupo_medio.setEnabled(False)
			self.sexo.setEnabled(False)
			self.apellido.setEnabled(False)
		else:
			self.grupo_medio.setEnabled(False)
			self.grupo_rubro.setEnabled(False)
		
	def guardar_contacto(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		tipo=self.tipo_contacto.currentText()
		if tipo=='Cliente':
			tipo_iva=self.tipo_iva.currentText()
			apellido=self.apellido.text()
			nombre=self.nombre.text()
			tipo_doc=self.tipo_doc.currentText()
			numero=self.numero.text()
			sexo=self.sexo.currentText()
			direccion=self.direccion.text()
			localidad=self.localidad.text()
			telefono=self.telefono.text()
			email=self.email.text()
			medio=self.medio_contacto.currentText()
			print(self.editar_contacto())
			if self.editar_contacto() == None or self.editar_contacto()==[]:
				datos=[tipo,tipo_iva,apellido,nombre, tipo_doc, numero,sexo, direccion,localidad, telefono, email,medio]
				if apellido == ''or nombre == '' or  numero == '' or direccion =='' or telefono =='':
					QMessageBox.warning(self, 'Error', 'Faltan datos')
				else:
					cursor.execute('INSERT INTO cliente VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?)', datos)
					conexion.commit()
					QMessageBox.information(self, "Nuevo contacto", "Se agregó correctamente el contacto" , QMessageBox.Ok, QMessageBox.Ok)
					self.limpiar_pantalla()
			else:
				cursor.execute('UPDATE cliente SET tipo=?, iva=?, apellido=?, nombre=?, tipo_doc=?, numero=?,sexo=?, direccion=?, localidad=?, telefono=?, email=?, contacto=? WHERE id=?',[tipo,tipo_iva,apellido,nombre, tipo_doc, numero,sexo, direccion,localidad, telefono, email,medio,(self.editar_contacto()[0][0])])
				conexion.commit()
				QMessageBox.information(self, "Modificacíon", "Se modificó correctamente el contacto" , QMessageBox.Ok, QMessageBox.Ok)
				self.limpiar_pantalla()
		elif tipo=='Proveedor':
			tipo_iva=self.tipo_iva.currentText()
			nombre=self.nombre.text()
			tipo_doc=self.tipo_doc.currentText()
			numero=self.numero.text()
			direccion=self.direccion.text()
			localidad=self.localidad.text()
			telefono=self.telefono.text()
			email=self.email.text()
			rubro=self.rubro.currentText()
			if self.editar_contacto() == None or self.editar_contacto()==[]:
				datos=[tipo,tipo_iva,nombre, tipo_doc, numero, direccion,localidad, telefono, email,rubro]
				if nombre == '' or  numero == '' or direccion =='' or telefono =='':
					QMessageBox.warning(self, 'Error', 'Faltan datos')
				else:
					cursor.execute('INSERT INTO proveedor VALUES(NULL,?,?,?,?,?,?,?,?,?,?)', datos)
					conexion.commit()
					QMessageBox.information(self, "Nuevo contacto", "Se agregó correctamente el contacto" , QMessageBox.Ok, QMessageBox.Ok)
					self.limpiar_pantalla()
			else:
				cursor.execute('UPDATE proveedor SET tipo=?, iva=?, nombre=?, tipo_doc=?, numero=?, direccion=?, localidad=?, telefono=?, email=?, rubro=? WHERE id=?',[tipo,tipo_iva,nombre, tipo_doc, numero, direccion,localidad, telefono, email,rubro,(self.editar_contacto()[0][0])])
				conexion.commit()
				QMessageBox.information(self, "Modificacíon", "Se modificó correctamente el contacto" , QMessageBox.Ok, QMessageBox.Ok)
				self.limpiar_pantalla()
		else:
			QMessageBox.warning(self, 'Error', 'Debe ingresar el tipo de contacto')
		conexion.close()

	def editar_contacto (self):
		self.lista_medios()
		self.lista_rubro()
		if self.numero.text()=='':
			QMessageBox.warning(self, 'Error', 'No se registran datos para editar.\nSeleccione un contacto y vuelva a intentarlo')
		else:
			self.nuevo_contacto.setEnabled(False)
			self.eliminar.setEnabled(False)
			conexion=sqlite3.connect('BD.db')
			cursor=conexion.cursor()
			tipo=self.tipo_contacto.currentText()
			if tipo=='Cliente': 
				numero=self.numero.text()
				cursor.execute('SELECT id FROM cliente WHERE numero=?',[numero])
				id_para_modificar=cursor.fetchall()
				self.guardar.setEnabled(True)
				self.grupo_contacto.setEnabled(True)
				self.tipo_contacto.setEnabled(True)
				self.tipo_iva.setEnabled(True)
				self.tipo_doc.setEnabled(True)
				self.numero.setEnabled(True)
				self.sexo.setEnabled(True)
				self.direccion.setEnabled(True)
				self.localidad.setEnabled(True)
				self.telefono.setEnabled(True)
				self.email.setEnabled(True)
				self.conf_contacto()
				return id_para_modificar
			elif tipo=='Proveedor': 
				numero=self.numero.text()
				cursor.execute('SELECT id FROM proveedor WHERE numero=?',[numero])
				id_para_modificar=cursor.fetchall()
				self.guardar.setEnabled(True)
				self.grupo_contacto.setEnabled(True)
				self.tipo_contacto.setEnabled(True)
				self.tipo_iva.setEnabled(True)
				self.tipo_doc.setEnabled(True)
				self.numero.setEnabled(True)
				self.direccion.setEnabled(True)
				self.localidad.setEnabled(True)
				self.telefono.setEnabled(True)
				self.email.setEnabled(True)
				self.conf_contacto()
				return id_para_modificar
			else:
				QMessageBox.warning(self, 'Error', 'Debe ingresar el tipo de contacto')
			conexion.close()

	def eliminar_contacto (self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		if self.editar_contacto() == None or self.editar_contacto()==[]:
			self.limpiar_pantalla()
			QMessageBox.warning(self, 'Error', 'No hay que eliminar')

		else:
			tipo=self.tipo_contacto.currentText()
			if tipo=='Cliente': 
				cursor.execute("DELETE FROM cliente WHERE id=(?)",[(self.editar_contacto()[0][0])])
				conexion.commit()
				conexion.close()
				QMessageBox.information(self, "Borrado", "Se borró correctamente el contacto" , QMessageBox.Ok, QMessageBox.Ok)
				self.limpiar_pantalla()
			elif tipo=='Proveedor': 
				cursor.execute("DELETE FROM proveedor WHERE id=(?)",[(self.editar_contacto()[0][0])])
				conexion.commit()
				conexion.close()
				QMessageBox.information(self, "Borrado", "Se borró correctamente el contacto" , QMessageBox.Ok, QMessageBox.Ok)
				self.limpiar_pantalla()
			else:
				QMessageBox.warning(self, 'Error', 'Debe ingresar el tipo de contacto')
		conexion.close()
	#Eliminar filas de tabla contactos
	def limpiar_filas(self):
		filas=self.tabla_contactos.rowCount()
		for i in range(filas):
			self.tabla_contactos.removeRow(0)
		self.tabla_contactos.clearContents()
				
	def limpiar_pantalla (self):
		self.nuevo_contacto.setEnabled(True)
		self.grupo_contacto.setEnabled(False)
		self.guardar.setEnabled(False)
		self.eliminar.setEnabled(False)
		self.modificar.setEnabled(False)
		self.buscador.setText('')	
		self.tipo_contacto.setCurrentText('')
		self.nombre.setText('')
		self.apellido.setText('')
		self.sexo.setCurrentText('')
		self.tipo_iva.setCurrentText('')
		self.tipo_doc.setCurrentText('')
		self.numero.setText('')
		self.direccion.setText('')
		self.localidad.setText('')
		self.telefono.setText('')
		self.email.setText('')
		self.medio_contacto.setCurrentText('')
		self.rubro.setCurrentText('')
		self.limpiar_filas()
		self.lista_medios()
		self.lista_rubro()

	#Listado de medios de contacto
	def lista_medios(self):
		self.medio_contacto.clear()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM medio_contacto ORDER by medio ASC')
		lista=[]
		for i in cursor.fetchall():
			lista.append(i[0])
		self.medio_contacto.addItems(lista)
		conexion.close()
	#Nuevo medio de contacto
	def agregar_medio(self):
		self.limpiar_pantalla()
		ventana=conf_medios(self)
		ventana.show()

	#Listado de sexo
	def lista_sexo(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM sexo')
		lista=[]
		for i in cursor.fetchall():
			lista.append(i[0])
		conexion.close()
		return lista
	
	#Listado de rubro proveedor
	def lista_rubro(self):
		self.rubro.clear()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM rubro ORDER by rubro ASC')
		lista=[]
		for i in cursor.fetchall():
			lista.append(i[0])
		self.rubro.addItems(lista)
		conexion.close()
			
	#Nuevo rubro
	def agregar_rubro(self):
		self.limpiar_pantalla()
		ventana=conf_rubros(self)
		ventana.show()
	
	#Listado de tipo de iva
	def lista_ivas(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM ivas')
		lista=[]
		for i in cursor.fetchall():
			lista.append(i[0])
		conexion.close()
		return lista

	def abrir_directorio(self):
		ventana=ventana_directorio(self)
		ventana.show()
'''
#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = ventana_agenda()
main.show()
sys.exit(app.exec_())'''