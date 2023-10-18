from array import array
from random import choice
import threading
import time

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Productor - Consumidor 1")
		self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

		self.w = QWidget(self)
		self.setCentralWidget(self.w)

		# Menu
		self.group_menu = QGroupBox('Menú', self)
		self.layout_group_menu = QFormLayout(self.group_menu)

		self.input_time_add = QDoubleSpinBox(self.group_menu)
		self.input_time_add.setRange(0.5, 2)
		self.input_time_add.setSingleStep(0.5)
		self.input_time_add.setDecimals(1)
		self.input_time_add.setMaximumWidth(100)
		
		self.layout_group_menu.addRow('Tiempo agregar: ', self.input_time_add)

		self.input_time_remove = QDoubleSpinBox(self.group_menu)
		self.input_time_remove.setRange(0.5, 2)
		self.input_time_remove.setSingleStep(0.5)
		self.input_time_remove.setDecimals(1)
		self.input_time_remove.setMaximumWidth(100)

		self.layout_group_menu.addRow('Tiempo remover: ', self.input_time_remove)
		# self.layout_group_menu.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
		self.group_menu.setMaximumSize(self.group_menu.minimumSizeHint())

		# Estacionamiento
		self.group_parking_lot = QGroupBox('Estacionamiento', self)
		self.layout_group_parking_lot = QVBoxLayout(self.group_parking_lot)
		self.parking_lot = ParkingLot(self.group_parking_lot, self)
		self.layout_group_parking_lot.addWidget(self.parking_lot)

		### LAYOUT PRINCIPAL ###
		self.layout = QVBoxLayout(self.w)
		self.layout.addWidget(self.group_menu)
		self.layout.addWidget(self.group_parking_lot)
		self.w.setLayout(self.layout)
		# self.setFixedSize(self.size())

		# Llamar hilos

		# Hilo para agregar coches
		add_thread = threading.Thread(target=self.parking_lot.addCar)
		add_thread.daemon = True # El hilo para cuando el main() se detiene
		add_thread.start()

		# Hilo para eliminar coches
		remove_thread = threading.Thread(target=self.parking_lot.removeCar)
		remove_thread.daemon = True # El hilo para cuando el main() se detiene
		remove_thread.start()

class ParkingLot(QWidget):
	def __init__(self, parent, mainWindow: MainWindow):
		super().__init__(parent)
		self.mainWindow = mainWindow
		self.setMinimumSize(500, 400)
		self.setMaximumSize(500, 400)

		# Pens
		self.pen_lines = QPen(QColorConstants.Yellow, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap)

		# Data
		self.parking = array('b', [False] * 10)
		self.occupied = []
		self.available = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

		mainWindow.input_time_add.setValue(choice([0.5, 1, 2]))
		mainWindow.input_time_remove.setValue(choice([0.5, 1, 2]))

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.fillRect(self.rect(), Qt.GlobalColor.black)
		
		# Dibujar celdas
		for y in range(2):
			for x in range(5):
				painter.fillRect(x * 100, y * 200, 100, 200, (QColorConstants.Red if self.parking[(5 * y) + x] else QColorConstants.Green))

		# Dibujar estacionamiento
		painter.setPen(self.pen_lines)
		for x in range(4):
			painter.drawLine((x * 100) + 100, 0, (x * 100) + 100, 400)
		painter.drawLine(0, 200, (4 * 100) + 100, 200)

	def addCar(self):
		while (True):
			if (len(self.available) != 0):
				index = choice(self.available)
				self.parking[index] = True
				self.available.remove(index)
				self.occupied.append(index)
				self.update()
			else:
				print('No hay espacio!!')
			
			time.sleep(self.mainWindow.input_time_add.value())

	def removeCar(self):
		while (True):
			if (len(self.occupied) != 0):
				index = choice(self.occupied)
				self.parking[index] = False
				self.occupied.remove(index)
				self.available.append(index)
				self.update()
			else:
				print('No quedan vehiculos!!')
			
			time.sleep(self.mainWindow.input_time_remove.value())

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
