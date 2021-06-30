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
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors, styles
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle
import os

class ventana_directorio(QMainWindow):
	clicked = pyqtSignal()
	def __init__(self, parent=None):
		super(ventana_directorio,self).__init__(parent)
		loadUi('visual/directorio.ui', self)
		
		#Filtro por tipo de cliente
		tipo_contacto=['Todos','Cliente', 'Proveedor']
		self.tipo_contacto.addItems(tipo_contacto)
		tipo=self.tipo_contacto.currentIndexChanged.connect(self.mostrar_directorio)
				
		# Establecer ancho de las columnas
		for indice, ancho in enumerate((40, 100, 150, 150, 80, 100, 120, 120, 120, 120), start=0):
			self.tabla_directorio.setColumnWidth(indice, ancho)

		#Señales de botonos
		#self.exp_pdf.clicked.connect(self.agenda_pdf)
		
		self.mostrar_directorio()

#Funciones
#Datos de agenda
	def mostrar_directorio(self):
		conexion=sqlite3.connect('BD.db')
		cursor=conexion.cursor()
		tipo=self.tipo_contacto.currentText()
		if tipo=='Cliente':
			self.tabla_directorio.clearContents()
			cursor.execute('SELECT * FROM cliente',)
			datos=cursor.fetchall()
			conexion.close()
		elif tipo=='Proveedor':
			self.tabla_directorio.clearContents()
			cursor.execute('SELECT *, NULL as apellido, NULL as sexo FROM proveedor',)
			datos=cursor.fetchall()
			conexion.close()
		else:
			self.tabla_directorio.clearContents()
			cursor.execute('SELECT * FROM cliente UNION ALL SELECT *,NULL as apellido, NULL as sexo FROM proveedor',)
			datos=cursor.fetchall()
			conexion.close()			
	
		n=0
		for i in datos:
			if i[11]!=None:
				self.tabla_directorio.setRowCount(n + 1)
				id_datos =QTableWidgetItem(str(i[0]))
				id_datos.setTextAlignment(QtCore.Qt.AlignCenter )
				self.tabla_directorio.setItem(n, 0, id_datos)
				self.tabla_directorio.setItem(n, 1, QTableWidgetItem(i[1]))
				self.tabla_directorio.setItem(n, 2, QTableWidgetItem(i[2]))
				self.tabla_directorio.setItem(n, 3, QTableWidgetItem(i[3]+', '+i[4]))
				self.tabla_directorio.setItem(n, 4, QTableWidgetItem(i[5]))
				self.tabla_directorio.setItem(n, 5, QTableWidgetItem(i[6]))
				self.tabla_directorio.setItem(n, 6, QTableWidgetItem(i[8]))
				self.tabla_directorio.setItem(n, 7, QTableWidgetItem(i[9]))
				self.tabla_directorio.setItem(n, 8, QTableWidgetItem(i[10]))
				self.tabla_directorio.setItem(n, 9, QTableWidgetItem(i[11]))
				n+=1
			else:
				self.tabla_directorio.setRowCount(n + 1)
				id_datos =QTableWidgetItem(str(i[0]))
				id_datos.setTextAlignment(QtCore.Qt.AlignCenter )
				self.tabla_directorio.setItem(n, 0, id_datos)
				self.tabla_directorio.setItem(n, 1, QTableWidgetItem(i[1]))
				self.tabla_directorio.setItem(n, 2, QTableWidgetItem(i[2]))
				self.tabla_directorio.setItem(n, 3, QTableWidgetItem(i[3]))
				self.tabla_directorio.setItem(n, 4, QTableWidgetItem(i[4]))
				self.tabla_directorio.setItem(n, 5, QTableWidgetItem(i[5]))
				self.tabla_directorio.setItem(n, 6, QTableWidgetItem(i[6]))
				self.tabla_directorio.setItem(n, 7, QTableWidgetItem(i[7]))
				self.tabla_directorio.setItem(n, 8, QTableWidgetItem(i[8]))
				self.tabla_directorio.setItem(n, 9, QTableWidgetItem(i[9]))
				n+=1
'''
#Exportar a PDF
	#Archivo 
	def agenda_pdf(self):
		#Id para nombre del archivo
		conexion=sqlite3.connect('teckelBD.db')
		cursor=conexion.cursor()
		tipo=self.tipo_contacto.currentText()
		#Nombre del archivo
		nombre='agenda'

		#Crear archivo pdf
		pdf=Canvas(f"archivos/pdf/{nombre}.pdf", pagesize=landscape(A4))#Tamaño A4 =595 x 842 px

					
		cliente=[]
		proveedor=[]
		todo=[]
		alfabeto=self.division_alfabetica(pdf)
		detalle=self.detalle_agenda(pdf)
		if tipo=='Cliente':
			cliente.append(detalle[0])
		elif tipo=='Proveedor':
			proveedor.append(detalle[1])
		else:
			cliente.append(detalle[0])
			proveedor.append(detalle[1])
		detalle=cliente+proveedor
		self.ensamblado(pdf,detalle)

		pdf.save()
		
		#archivo= QMessageBox.question(self, 'Mensaje PyQt5', "¿Te gusta PyQt5??", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		#if archivo == QMessageBox.Yes:
	#	os.system(f"I:/Martin/Proyectos_programacion/Sistema_basico/windows/archivos/pdf/{nombre}.pdf")
	#	else:
	#		pass
	
	#Encabezado
	def encabezado_pdf(self,pdf):
		alto=595
		ancho=842
		pdf.setStrokeColorRGB(0,0,0)
		pdf.setLineWidth(3)#ancho de la linea
		pdf.roundRect(ancho-ancho+15,alto-55,812,40,0,stroke = 1, fill=0)
		pdf.drawCentredString((ancho/2)-3,alto-55+15,"AGENDA")

	def subtitulo_pdf(self, pdf):
		conexion=sqlite3.connect('teckelBD.db')
		cursor=conexion.cursor()
		tipo=self.tipo_contacto.currentText()
		if tipo=='Cliente':
			alto=595
			ancho=842
			pdf.setStrokeColorRGB(0,0,0)
			pdf.setLineWidth(3)#ancho de la linea
			pdf.roundRect(ancho-ancho+15,alto-90,812,30,0,stroke = 1, fill=0)
			pdf.drawCentredString((ancho/2)-3,alto-90+15,"Cliente")
		elif tipo=='Proveedor':
			alto=595
			ancho=842
			pdf.setStrokeColorRGB(0,0,0)
			pdf.setLineWidth(3)#ancho de la linea
			pdf.roundRect(ancho-ancho+15,alto-90,812,30,0,stroke = 1, fill=0)
			pdf.drawCentredString((ancho/2)-3,alto-90+15,"Proveedor")

		else:
			print('Configurar si es "Todos"')
	
	#Conteo de items en la agenda
	def cantidad_contactos(self):
		tipo=self.tipo_contacto.currentText()
		conexion=sqlite3.connect('teckelBD.db')
		cursor=conexion.cursor()
		#Seleccion de las iniciales disponibles de clientes
		cursor.execute('SELECT id FROM cliente ')
		resultado=cursor.fetchall()
		cantidad_cliente=len(resultado)

		cursor.execute('SELECT id FROM proveedor')
		resultado=cursor.fetchall()
		cantidad_proveedor=len(resultado)

		return [cantidad_cliente]+[cantidad_proveedor]

	#Division alfabetica
	def division_alfabetica(self,pdf):
		conexion=sqlite3.connect('teckelBD.db')
		cursor=conexion.cursor()
		tipo=self.tipo_contacto.currentText()
		#Seleccion de las iniciales disponibles de clientes
		cursor.execute('SELECT apellido FROM cliente ORDER BY apellido ASC',)
		primer_letra=[]
		for i in cursor.fetchall():
			primer_letra.append(i[0][0])
		alfabeto_cliente=sorted(set(primer_letra))#SORTED:ordenamos las letras alfabeticamente. SET:elimina los repetidos(de forma desordenada)
		
		#Seleccion de las iniciales disponibles de proveedores
		cursor.execute('SELECT nombre FROM proveedor ORDER BY nombre ASC',)
		primer_letra=[]
		for i in cursor.fetchall():
			primer_letra.append(i[0][0])
		alfabeto_proveedor=sorted(set(primer_letra))#SORTED:ordenamos las letras alfabeticamente. SET:elimina los repetidos(de forma desordenada)
		
		return alfabeto_cliente,alfabeto_proveedor

	#Datos de agenda:
	def detalle_agenda(self, pdf):
		conexion=sqlite3.connect('teckelBD.db')
		cursor=conexion.cursor()
		tipo=self.tipo_contacto.currentText()
		alfabeto=self.division_alfabetica(pdf)
		
		#Listas de clientes ordenados alfabeticamente
		listado_cliente=[]
		cursor.execute('SELECT apellido,nombre,direccion, localidad, telefono,email FROM cliente ORDER BY apellido, nombre ASC')
		resultado=[]
		for i in cursor.fetchall():
			resultado.append(i[0]+', '+i[1])# unimos apellido y nombre en un item
			resultado.append(i[2]+ ' - '+ i[3]) #unimos direccion y localidad en un item
			resultado.append(i[4])
			resultado.append(i[5])
		n=4
		ordenado=[resultado[i:i+n] for i in range(0, len(resultado),n)]#separar los datos de los diferentes contactos en listas individuales
		listado_cliente=ordenado
		
		#Listas de proveedores ordenados alfabeticamente
		listado_proveedor=[]
		cursor.execute('SELECT nombre,direccion, localidad, telefono,email FROM proveedor ORDER BY nombre ASC')
		resultado=[]
		for i in cursor.fetchall():
			resultado.append(i[0])
			resultado.append(i[1]+ ' - '+ i[2]) #unimos direccion y localidad en un item
			resultado.append(i[3])
			resultado.append(i[4])
		n=4
		ordenado=[resultado[i:i+n] for i in range(0, len(resultado),n)]#separar los datos de los diferentes contactos en listas individuales
		listado_proveedor=ordenado
		
		return [listado_cliente]+[listado_proveedor]

	def ensamblado(self, pdf, detalle):
		#Generación de lista de PDF
		min=0 #inicio de la lista
		max=26 #final de la lista
		c=26 #Elementos por lista
		#datos de listas 
		print(detalle[0])
		#print(self.cantidad_contactos())
		tipo=self.tipo_contacto.currentText()
		if tipo=='Cliente':
			div=(len(detalle[0])//c) #Cantidad de listas
			r=0 #Repetición del bucle
			s=(len(detalle)%c) #Elementos libres
			while len(detalle)%c!=0 and len(detalle)>=c:
				self.encabezado_pdf(pdf)
				self.subtitulo_pdf(pdf)
				self.detalle_pdf(pdf, detalle[min:max],len(detalle))
				min+=c
				max+=c
				r+=1
				pdf.showPage()
				if r==div:
					self.encabezado_pdf(pdf)
					self.subtitulo_pdf(pdf)
					self.detalle_pdf(pdf, detalle[min:min+s],len(detalle))
					break
			while len(detalle)%c==0 :
				self.encabezado_pdf(pdf)
				self.subtitulo_pdf(pdf)
				self.detalle_pdf(pdf, detalle[min:max],len(detalle))
				min+=c
				max+=c
				r+=1
				pdf.showPage()
				if r==div:
					break
			if len(detalle[0])<c:
				self.encabezado_pdf(pdf)
				self.subtitulo_pdf(pdf)
				self.cabecera_tabla_pdf(pdf)
				n=0
				for i in detalle:
					print(i)
					print(self.detalle_pdf(pdf, i,len(detalle)))
					self.detalle_pdf(pdf, i,len(detalle))
					n+=1
		elif tipo=='Proveedor':
			self.encabezado_pdf(pdf)
			self.subtitulo_pdf(pdf)
			print('No pasa nada carnal')
		else:
			self.encabezado_pdf(pdf)
			self.subtitulo_pdf(pdf)
			print('No pasa nada brody')

	#Cabecera de tabla
	def cabecera_tabla_pdf(self,pdf):
		#Tabla con detalle de pedido
		width, height = A4
		columnas=[
			['Nombre','Dirección', 'Telefono', 'Email'],
			]
		cabecera=Table(columnas, colWidths=[150,200,180,150],rowHeights=20)
		cabecera.setStyle(TableStyle([
			('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones verticales
			('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #recuadro del la tabla
			('LINEBELOW',(0,0), (-1,-1), 1,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones horizontales
			('LINEBELOW',(0,0), (-1,0), 2,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)) #division entre cabecera y detalle
			]))
		cabecera.wrapOn(pdf, width, height)
		w,h=cabecera.wrap(0,0)
		cabecera.drawOn(pdf, 40,height-(842-(20*(24))))
	#Detalle
	def detalle_pdf(self,pdf, detalle,n):
		#Tabla con detalle de pedido
		width, height = A4
		pedido=Table(detalle, colWidths=[150,200,180,150],rowHeights=20)
		pedido.setStyle(TableStyle([
			('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones verticales
			('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #recuadro del la tabla
			('LINEBELOW',(0,0), (-1,-1), 1,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones horizontales
			('LINEBELOW',(0,0), (-1,0), 1,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)) #division entre detalle
			]))
		
		pedido.wrapOn(pdf, width, height)
		w,h=pedido.wrap(0,0)
		pedido.drawOn(pdf, 40,height-(842-(20*(21-n))))'''
		

'''
	

#Exportar a Excel

	def exportar_directorio_excel(self):
		cursor.execute("SELECT * FROM pedidos ORDER BY id DESC LIMIT 1")
		id_pedido=[]
		for i in cursor.fetchall():
			id_pedido.append(i[0])			
		conexion.commit()
		id_pedido=id_pedido[0]
		nombre=str(f'N° {id_pedido} - {self.cliente.get()}')
		archivo = Workbook()
		hoja=archivo.active
		hoja['B2']='Pedido N°: '
		hoja['B3']=id_pedido
		hoja['C2']='Fecha:'
		hoja['C3']=self.fecha
		hoja['D2']='Cliente:'
		hoja['D3']=self.cliente.get()
		hoja['B5']='Sub-Total: '
		hoja['B6']=self.subtotal.get()
		hoja['C5']= 'Porcentaje dto:'
		hoja['C6']=	self.porcentaje_descuento.get()
		hoja['D5']='Monto de Descuento:'
		hoja['D6']=self.descuento.get()
		hoja['E5']='Envio:'
		hoja['E6']=self.envio.get()
		hoja['B8']='Total:'
		hoja['B9']=self.total_pedido.get()
		hoja['D8']='Recargo:'
		hoja['D9']=self.recargo.get()
		
		hoja['B10']=''
		hoja.append(['id','producto', 'cant.', 'precio_venta', 'pretotal'])
		tabla=cursor.execute('SELECT * FROM temporalpedido')
		for i in tabla:
			hoja.append(i)

		#Ajuste de ancho de columnas
		for i in hoja.columns:
			ancho = 0
			columna = i[0].column_letter
			for celda in i:
				try:
					if len(str(celda.value)) > ancho:
						ancho = len(celda.value)
				except:
					pass
			ajuste_celda = (ancho + 2) * 1.2
			hoja.column_dimensions[columna].width = ajuste_celda
		archivo.save(f"./Pedidos/{nombre}.xlsx")
		
		'''
'''#Cierre de la app para que se ejecute
app = QApplication(sys.argv)
app.setStyle('Fusion')
main = ventana_directorio()
main.show()
sys.exit(app.exec_())'''