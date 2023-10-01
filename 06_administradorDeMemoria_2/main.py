import os
os.add_dll_directory('C:/mingw64/bin')

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from memory_manager_2 import Process, Manager, Algorithm, process_from_file

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
		factor = (self.height() - (4 * len(self.manager.memory))) / totalHeight

		# Pens
		pen_rect = QPen(QColorConstants.Black, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
		pen_text = QPen(QColorConstants.Black)

		# Colores
		currentColor = True
		color1 = QColor(204, 204, 255)
		color2 = QColor(204, 255, 255)
		
		y = 0
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
			y += height + 4

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Administrador de memoria 2")
		self.setGeometry(0, 0, 400, 500)

		self.w = QWidget(self)
		# self.w.setStyleSheet("background-color: white;")
		self.setCentralWidget(self.w)

		# Memory manager
		self.manager = Manager([1000, 400, 1800, 700, 900, 1200, 1500])

		# Menu file
		open_action_file = QAction('Abrir archivo', self)
		open_action_file.triggered.connect(self.open_file)

		open_action_list = QAction('Abrir lista', self)
		open_action_list.triggered.connect(self.open_list)

		file_menu = self.menuBar().addMenu('Archivo')
		file_menu.addAction(open_action_file)
		file_menu.addAction(open_action_list)

		### Grupo agregar memoria ###
		self.group_add_memory = QGroupBox('Agregar memoria', self)
		self.layout_group_add_memory = QFormLayout(self.group_add_memory)

		# Menu agregar memoria
		self.input_memory_size = QSpinBox(self.group_add_memory)
		self.input_memory_size.setMinimum(1)
		self.input_memory_size.setMaximum(9999999)
		self.input_memory_position = QCheckBox(self.group_add_memory)
		self.button_add_memory = QPushButton('Agregar bloque de memoria', self.group_add_memory)
		self.button_add_memory.clicked.connect(lambda: self.add_memory(self.input_memory_size.value(), self.input_memory_position.isChecked()))
		
		# Layout
		self.layout_group_add_memory.addRow(QLabel('Tamaño', self.group_add_memory), self.input_memory_size)
		self.layout_group_add_memory.addRow(QLabel('Al final', self.group_add_memory), self.input_memory_position)
		self.layout_group_add_memory.addRow(self.button_add_memory)

		### Grupo agregar archivo ###
		self.group_add_process = QGroupBox('Agregar archivo', self)
		self.layout_group_add_memory = QFormLayout(self.group_add_process)

		# Menu agregar archivo
		self.input_process_name = QLineEdit(self.group_add_process)
		self.input_process_size = QSpinBox(self.group_add_process)
		self.input_process_size.setMinimum(1)
		self.input_process_size.setMaximum(9999999)
		self.button_add_process = QPushButton('Agregar archivo', self.group_add_process)
		self.button_add_process.clicked.connect(lambda: self.add_process(Process(self.input_process_name.text(), self.input_process_size.value())))
		
		# Layout
		self.layout_group_add_memory.addRow(QLabel('Nombre', self.group_add_process), self.input_process_name)
		self.layout_group_add_memory.addRow(QLabel('Tamaño', self.group_add_process), self.input_process_size)
		self.layout_group_add_memory.addRow(self.button_add_process)

		### Grupo algoritmo ###
		self.group_change_algorithm = QGroupBox('Cambiar algoritmo', self)
		self.layout_group_change_algorithm = QFormLayout(self.group_change_algorithm)

		# Combobox algoritmo
		self.combobox_algorithm = QComboBox(self.group_change_algorithm)
		self.combobox_algorithm.addItem("Primer ajuste")
		self.combobox_algorithm.addItem("Mejor ajuste")
		self.combobox_algorithm.addItem("Peor ajuste")
		self.combobox_algorithm.addItem("Siguiente ajuste")
		self.combobox_algorithm.activated.connect(self.change_algorithm)

		# Layout
		self.layout_group_change_algorithm.addWidget(self.combobox_algorithm)

		### Grupo dibujo ###
		self.group_draw = QGroupBox("Dibujo", self)
		self.layout_group_draw = QVBoxLayout(self.group_draw)

		# Painter
		self.painter = MemoryPainter(self.manager, self.group_draw)

		# Layout
		self.layout_group_draw.addWidget(self.painter)
		
		### LAYOUT PRINCIPAL ###
		self.container_left = QWidget(self.w)
		self.container_left.setMaximumWidth(300)
		self.layout_left = QVBoxLayout(self.container_left)
		self.layout_left.addWidget(self.group_add_memory)
		self.layout_left.addWidget(self.group_add_process)
		self.layout_left.addWidget(self.group_change_algorithm)

		self.container_right = QWidget(self.w)
		self.layout_right = QVBoxLayout(self.container_right)
		self.layout_right.addWidget(self.group_draw)

		self.layout = QHBoxLayout(self.w)
		self.layout.addWidget(self.container_left)
		self.layout.addWidget(self.container_right)
		self.w.setLayout(self.layout)

	def open_file(self):
		file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de Texto (*.txt);;Todos los archivos (*)')
		if file_name:
			size = int(os.path.getsize(file_name) / 1000)
			self.manager.insert_process(Process(os.path.basename(file_name), size))

	def open_list(self):
		file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de Texto (*.txt);;Todos los archivos (*)')
		if file_name:
			process = process_from_file(file_name)
			self.manager.insert_process(process)

	def change_algorithm(self):
		self.manager.algorithm = Algorithm(self.combobox_algorithm.currentIndex())
		self.manager.refresh()
		self.painter.update()

	def add_memory(self, size: int, end: bool):
		self.manager.add_memory(size, end)
		self.painter.update()

	def add_process(self, p: Process):
		self.manager.insert_process(p)
		self.painter.update()

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
