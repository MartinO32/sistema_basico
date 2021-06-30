import sys
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QCompleter, QDialog, QListWidgetItem, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from _sqlite3 import Error, IntegrityError
import sqlite3
from PyQt5 import Qt, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
import time
from inicio import Inicio
import socket

class login (QDialog):
	pasar_usuario = pyqtSignal()

	def __init__(self, parent=None):
		super(login, self).__init__(parent)
		loadUi('visual/login.ui', self)

		#Señales de botones
		self.aceptar.clicked.connect(self.iniciar)
		self.nuevo_usuario.clicked.connect(self.crear_usuario)
		self.cambio_pass.clicked.connect(self.cambiar)
		self.ver_pass.setCheckable(True)
		self.ver_pass.pressed.connect(self.mostrar_pass)
		
		#Autocompletar usuarios disponibles												 
		usuarios = self.usuarios_disponibles()
		autocompletar = QCompleter(usuarios)
		self.usuario.setCompleter(autocompletar)
		
#Funciones de Botones
	#Inicio de sesion
	def iniciar(self):
		terminal=socket.gethostname()
		usuario=self.usuario.text()
		passw=self.password.text()
		acceso=time.strftime("%d/%m/%y %H:%M:%S")
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM login WHERE usuario=?',[usuario])
		resultado=cursor.fetchall()
		if resultado==[]:
			QMessageBox.warning(self, 'Error','Usuario inexistente')
			self.usuario.setText('')
			self.usuario.setFocus()
			self.password.setText('')
		elif resultado[0][3]!=passw:	
			QMessageBox.warning(self, 'Error','Contraseña incorrecta')
			self.password.setText('')
		else:
			cursor.execute('SELECT * FROM usuario_activo WHERE usuario=?', [usuario])
			consulta=cursor.fetchone()
			
			if consulta==None:
				cursor.execute('INSERT INTO usuario_activo VALUES (?,?,?)',[usuario,terminal,acceso])
				conexion.commit()
				conexion.close()
				self.hide()
				ventana=Inicio(self)
				ventana.show()
			elif usuario==consulta[0] and terminal!=consulta[1]:
				QMessageBox.warning(self, 'Error', f'El usuario\t"{usuario}"\tes encuentra activo en la PC\t"{consulta[1]}".\n\nCierre el mismo y vuelva a intentarlo')
				self.close()
			else:
				cursor.execute('UPDATE usuario_activo SET ingreso=? WHERE usuario=?',(acceso,usuario))
				conexion.commit()
				conexion.close()
				self.hide()
				ventana=Inicio(self)
				ventana.show()
	
	#Nuevo usuario
	def crear_usuario(self):
		ventana=ventana_nuevo(self)
		ventana.show()

	#Cambiar contraseña
	def cambiar(self):
		ventana=ventana_cambio(self)
		ventana.show()

	#Usuarios disponibles
	def usuarios_disponibles (self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT usuario FROM login')
		resultado=[]
		for i in cursor.fetchall():
			resultado.append(i[0])
		return resultado
	
	#Mostrar contraseña que se escribió
	def mostrar_pass (self):
		if self.ver_pass.isChecked():
			self.password.setEchoMode(QtWidgets.QLineEdit.Password)
		else:
			self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
		
		
class ventana_nuevo(QDialog):
	def __init__(self, parent=None):
		super(ventana_nuevo, self).__init__(parent)
		loadUi('../visual/nuevo_usuario.ui', self)

		self.aceptar_nuevo.clicked.connect(self.guardar_usuario)

# Funciones de botones
	#Nuevo usuario
	def guardar_usuario (self):
		nombre=self.nombre.text()
		usuario=self.usuario.text()
		passw=self.password.text()
		acceso=time.strftime("%d/%m/%y %H:%M:%S")
		conf_pass=self.confirmacion_pass_nuevo.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM login WHERE nombre=?',[nombre])
		resultado=cursor.fetchall()
		if passw==conf_pass:
			if resultado==[]:
				cursor.execute('INSERT INTO login VALUES (NULL,?,?,?,?)', [nombre, usuario, passw])
				conexion.commit()
				conexion.close()
				QMessageBox.information(self, 'Correcto','Se creo nuevo usuario correctamente', QMessageBox.Ok, QMessageBox.Ok)
				self.nombre.setText('')
				self.usuario.setText('')
				self.password.setText('')
				self.confirmacion_pass_nuevo.setText('')
			else:
				QMessageBox.warning(self, 'Existente',f'El nombre que intenta agregar,\nya dispone de usuario y es: "{resultado[0][2]}"')	
				self.usuario.setText('')
				self.password.setText('')
				self.confirmacion_pass_nuevo.setText('')
		else:
			QMessageBox.warning(self, 'Error','Las contraseñas no coinciden' )	
			self.password.setText('')
			self.confirmacion_pass_nuevo.setText('')
		
class ventana_cambio(QDialog):
	def __init__(self, parent=None):
		super(ventana_cambio, self).__init__(parent)
		loadUi('../visual/cambio_pass.ui', self)

	#señales de botones
		self.aceptar_cambio.clicked.connect(self.cambiar_pass)

	#Autocompletar usuarios disponibles												 
		usuarios = self.usuarios_disponibles()
		autocompletar = QCompleter(usuarios)
		self.usuario_cambio_pass.setCompleter(autocompletar)

# Funciones de botones
	#Cambio de contraseña
	def cambiar_pass(self):
		usuario=self.usuario_cambio_pass.text()
		pass_actual=self.pass_actual.text()
		pass_nuevo=self.pass_nuevo.text()
		acceso=time.strftime("%d/%m/%y %H:%M:%S")
		confirmacion_pass_nuevo=self.confirmacion_pass_nuevo.text()
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT * FROM login WHERE usuario=?',[usuario])
		resultado=cursor.fetchall()	
		if resultado[0][2]!=usuario or resultado==[]:
			QMessageBox.warning(self,'Error','El usuario es incorrecto')
			self.usuario_cambio_pass.setText('')
			self.usuario_cambio_pass.setFocus()
			self.pass_actual.setText('')
			self.pass_nuevo.setText('')
			self.confirmacion_pass_nuevo.setText('')
		elif resultado[0][3]!=pass_actual:
			QMessageBox.warning(self,'Error','La contraseña actual es incorrecta')
			self.pass_actual.setText('')
			self.pass_actual.setFocus()
			self.pass_nuevo.setText('')
			self.confirmacion_pass_nuevo.setText('')
		elif pass_nuevo!=confirmacion_pass_nuevo:
			QMessageBox.warning(self,'Error','Las contraseñas ingresadas son diferentes')
			self.pass_nuevo.setText('')
			self.pass_nuevo.setFocus()
			self.confirmacion_pass_nuevo.setText('')
		else:
			cursor.execute('UPDATE login SET passw=?, ingreso=? WHERE usuario=?',(pass_nuevo,acceso,usuario))
			conexion.commit()
			conexion.close()
			QMessageBox.information(self,'Correcto', 'Se modificó satisfactoriamente la contraseña')
			self.usuario_cambio_pass.setText('')
			self.usuario_cambio_pass.setFocus()
			self.pass_actual.setText('')
			self.pass_nuevo.setText('')
			self.confirmacion_pass_nuevo.setText('')
		
	#Usuarios disponibles
	def usuarios_disponibles (self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		cursor.execute('SELECT usuario FROM login')
		resultado=[]
		for i in cursor.fetchall():
			resultado.append(i[0])
		return resultado

app = QApplication(sys.argv)
app.setStyle('Fusion')
main = login() 
main.show()
sys.exit(app.exec_())