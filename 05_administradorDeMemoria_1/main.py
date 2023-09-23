import os
os.add_dll_directory('C:/mingw64/bin')

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from memory_manager import Manager, Algorithm, process_from_file

class MemoryPainter(QWidget):
	def __init__(self, manager, parent=None):
		super().__init__(parent)
		self.setMinimumSize(400, 400)
		self.manager = manager

		self.font_normal = QFont("Consolas", 12)
		self.font_big = QFont("Consolas", 18)


	def paintEvent(self, event):
		painter = QPainter(self)

		# Pintar
		width = int(self.width() * 0.6)
		totalHeight = sum(memory_block.totalSize for memory_block in self.manager.memory)
		factor = (self.height() * 0.9) / totalHeight

		# Colores
		currentColor = True
		color1 = QColor(204, 204, 255)
		color2 = QColor(204, 255, 255)
		
		
		y = 10
		for i in range(len(self.manager.memory)):
			
			painter.setPen(QPen(QColorConstants.Black, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
			x = int((self.width() / 2) - (width / 2))

			# Dibujar los bloques de memoria
			height = int(self.manager.memory[i].totalSize * factor)
			painter.fillRect(x, y, width, height, QColorConstants.Black)

			# Numero del bloque
			painter.setPen(QPen(QColorConstants.Black))
			painter.setFont(self.font_big)
			painter.drawText(x - 50, y + 18, f"[{i}]")
			painter.drawText(x + width, y + 18, f"[{self.manager.memory[i].totalSize}]")
			painter.setPen(QPen(QColorConstants.Black, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

			# Dibujar los procesos (espacio utilizado)
			process_y = y
			for j in range(len(self.manager.memory[i].process)):
				process_height = int(self.manager.memory[i].process[j].size * factor)
				painter.fillRect(x, process_y, width, process_height, (color1 if currentColor else color2))
				currentColor = not currentColor

				# Dibujar datos del proceso
				painter.setPen(QPen(QColorConstants.Black))
				painter.setFont(self.font_normal)
				painter.drawText(x + 8, process_y + 14, f"{self.manager.memory[i].process[j].name}:  {self.manager.memory[i].process[j].size}kb")
				painter.setPen(QPen(QColorConstants.Black, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

				process_y += process_height

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
		process = process_from_file('archivos.txt')
		self.manager = Manager([1000, 400, 1800, 700, 900, 1200, 1500])
		self.manager.algorithm = Algorithm.MEJOR_AJUSTE
		self.manager.insert_process(process)
		print(self.manager)

		# Menu file
		open_action = QAction('Abrir', self)

		file_menu = self.menuBar().addMenu('Archivo')
		file_menu.addAction(open_action)

		# Grupo
		self.group = QGroupBox("Memoria", self)
		self.layout_group_form = QVBoxLayout(self.group)

		# Painter
		self.painter = MemoryPainter(self.manager, self.group)
		self.layout_group_form.addWidget(self.painter)
		
		# Agregar al layout principal
		self.layout.addWidget(self.group)
		self.w.setLayout(self.layout)

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
