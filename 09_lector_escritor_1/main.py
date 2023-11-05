import sys
import random
import time
import threading

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

WRITING = False

# Cuantos estan leyendo en el momento
READING = 0

class FileReadThread(QThread):
	signal = pyqtSignal(str)

	def __init__(self):
		super().__init__()

	def run(self):
		global WRITING
		global READING

		READING += 1

		self.signal.emit('')
		file = open('file.txt', 'r')
		char = file.read(1)

		while char:
			self.signal.emit(char)
			char = file.read(1)
			time.sleep(0.1)

		READING -= 1

class FileWriteThread(QThread):
	signal = pyqtSignal()

	def __init__(self, text: QTextEdit):
		super().__init__()
		self.txt = text

	def run(self):
		global WRITING
		global READING

		WRITING = True

		new_text = self.txt.toPlainText()

		while self.txt.toPlainText():
			self.signal.emit()
			time.sleep(0.1)

		file = open('file.txt', 'w')
		file.write(new_text)

		WRITING = False

class MainWindow(QMainWindow):
	def __init__(self, title: str):
		super().__init__()

		self.setGeometry(0, 0, 300, 300)
		self.setFixedSize(300, 300)
		self.setWindowTitle(title)
		self.w = QWidget(self)
		self.setCentralWidget(self.w)

		# Menu file
		action_read = QAction('Leer', self)
		action_read.triggered.connect(self.read)

		action_save = QAction('Guardar', self)
		action_save.triggered.connect(self.save)

		file_menu = self.menuBar().addMenu('Acciones')
		file_menu.addAction(action_read)
		file_menu.addAction(action_save)

		# Contenido
		self.group_content = QGroupBox(self)
		self.layout_group_content = QVBoxLayout(self.group_content)

		self.edit = QCheckBox('Editar', self.group_content)
		self.edit.clicked.connect(self.change_mode)

		self.txt = QTextEdit(self.group_content)
		self.txt.setReadOnly(True)

		self.layout_group_content.addWidget(self.edit)
		self.layout_group_content.addWidget(self.txt)

		### LAYOUT PRINCIPAL ###
		self.layout = QVBoxLayout(self.w)
		self.layout.addWidget(self.group_content)
		self.w.setLayout(self.layout)

	def read(self):

		global WRITING
		global READING

		if WRITING:
			print('Error: el archivo está ocupado')
		else:
			self.read_thread = FileReadThread()
			self.read_thread.signal.connect(self.update_text)
			self.read_thread.start()

	def update_text(self, char):
		if (char == ''):
			self.txt.clear()

		self.txt.setPlainText(self.txt.toPlainText() + char)


	def save(self):
		if WRITING or READING > 0:
			print('Error: el archivo está ocupado')
		else:
			self.write_thread = FileWriteThread(self.txt)
			self.write_thread.signal.connect(self.write_text)
			self.write_thread.start()

	def write_text(self):
		current_text = self.txt.toPlainText()
		updated_text = current_text[1:]
		self.txt.setPlainText(updated_text)

	def change_mode(self):
		global WRITING
		global READING

		if (self.edit.isChecked()):
			if (WRITING):
				print('Error: el archivo está ocupado')
				self.edit.setChecked(False)
			else:
				WRITING = True
				self.txt.setReadOnly(False)
		else:
			WRITING = False
			self.txt.setReadOnly(True)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	w1 = MainWindow('Ventana 1')
	w2 = MainWindow('Ventana 2')
	w3 = MainWindow('Ventana 3')

	w1.show()
	w2.show()
	w3.show()

	sys.exit(app.exec())
