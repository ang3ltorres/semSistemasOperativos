import os
os.add_dll_directory('C:/mingw64/bin')

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from memory_manager_2 import Manager, Algorithm, process_from_file

class MemoryPainter(QWidget):
	def __init__(self, manager, parent=None):
		super().__init__(parent)
		self.setMinimumSize(400, 400)
		self.manager = manager

		self.font_normal = QFont("Consolas", 12)
		self.font_big = QFont("Consolas", 18)


	def paintEvent(self, event):
		painter = QPainter(self)

		# Calculos
		width = int(self.width() * 0.6)
		totalHeight = sum(memory_block.totalSize for memory_block in self.manager.memory)
		factor = (self.height() * 0.9) / totalHeight

		# Pens
		pen_rect = QPen(QColorConstants.Black, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
		pen_text = QPen(QColorConstants.Black)

		# Colores
		currentColor = True
		color1 = QColor(204, 204, 255)
		color2 = QColor(204, 255, 255)
		
		y = 10
		for i in range(len(self.manager.memory)):
			
			painter.setPen(pen_rect)
			x = int((self.width() / 2) - (width / 2))

			# Dibujar los bloques de memoria
			height = int(self.manager.memory[i].totalSize * factor)
			painter.fillRect(x, y, width, height, QColorConstants.Black)

			# Numero y size del bloque
			painter.setPen(pen_text)
			painter.setFont(self.font_big)
			painter.drawText(x - 50, y + 18, f"[{i}]")
			painter.drawText(x + width, y + 18, f"[{self.manager.memory[i].totalSize}kb]")
			painter.setPen(pen_rect)

			# Dibujar los procesos (espacio utilizado)
			process_y = y
			for j in range(len(self.manager.memory[i].process)):
				process_height = int(self.manager.memory[i].process[j].size * factor)
				painter.fillRect(x, process_y, width, process_height, (color1 if currentColor else color2))
				currentColor = not currentColor

				# Dibujar datos del proceso
				painter.setPen(pen_text)
				painter.setFont(self.font_normal)
				painter.drawText(x + 8, process_y + 14, f"{self.manager.memory[i].process[j].name}:  {self.manager.memory[i].process[j].size}kb")

				process_y += process_height

			painter.setPen(pen_rect)
			painter.drawRect(x, y, width, height)
			y += height + 8

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Administración de memoria")
		self.setGeometry(0, 0, 400, 500)

		self.w = QWidget(self)
		self.w.setStyleSheet("background-color: white;")
		self.setCentralWidget(self.w)
		self.layout = QVBoxLayout(self.w)

		# Memory manager
		self.manager = Manager([1000, 400, 1800, 700, 900, 1200, 1500])

		# Menu file
		open_action = QAction('Abrir', self)
		open_action.triggered.connect(self.open_file)

		file_menu = self.menuBar().addMenu('Archivo')
		file_menu.addAction(open_action)

		# Grupo
		self.group = QGroupBox("Memoria", self)
		self.layout_group_form = QVBoxLayout(self.group)

		self.combobox_algorithm = QComboBox(self.group)
		self.combobox_algorithm.addItem("Primer ajuste")
		self.combobox_algorithm.addItem("Mejor ajuste")
		self.combobox_algorithm.addItem("Peor ajuste")
		self.combobox_algorithm.addItem("Siguiente ajuste")
		self.combobox_algorithm.activated.connect(self.change_algorithm)

		# Painter
		self.painter = MemoryPainter(self.manager, self.group)

		# Layout
		self.layout_group_form.addWidget(self.combobox_algorithm)
		self.layout_group_form.addWidget(self.painter)
		
		# Agregar al layout principal
		self.layout.addWidget(self.group)
		self.w.setLayout(self.layout)

	def open_file(self):
		file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de Texto (*.txt);;Todos los archivos (*)')
		if file_name:
			process = process_from_file('archivos.txt')
			self.manager.insert_process(process)

	def change_algorithm(self):
		self.manager.algorithm = Algorithm(self.combobox_algorithm.currentIndex())
		self.manager.refresh()
		self.painter.update()

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
