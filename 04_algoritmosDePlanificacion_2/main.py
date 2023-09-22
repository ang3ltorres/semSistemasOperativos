import sys
import os
import time
from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
os.add_dll_directory('C:/mingw64/bin')
from processManager import Process, OrderBy, Manager, Algorithm

class ThreadTable(QThread):
	signal = pyqtSignal()
	finished_signal = pyqtSignal()

	def __init__(self, window, parent=None):
		super().__init__(parent)
		self.window = window
		self.stop = False

	def run(self):
		while (self.window.manager.consume() and not self.stop):
			self.signal.emit()
			self.msleep(500)

		self.finished_signal.emit()

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Algoritmos de planificación")
		self.setGeometry(0, 0, 400, 500)

		self.w = QWidget(self)
		self.setCentralWidget(self.w)
		self.layout = QVBoxLayout(self.w)

		# Menu file
		open_action = QAction('Abrir', self)
		open_action.triggered.connect(self.open_file)

		file_menu = self.menuBar().addMenu('Archivo')
		file_menu.addAction(open_action)

		# Grupo agregar proceso
		self.group_form = QGroupBox("Agregar proceso", self)
		self.layout_group_form = QGridLayout(self.group_form)

		self.label_process_name = QLabel("Nombre", self.group_form)
		self.entry_process_name = QLineEdit(self.group_form)
		self.label_process_time = QLabel("Tiempo", self.group_form)
		self.entry_process_time = QSpinBox(self.group_form)
		self.label_process_priority = QLabel("Prioridad", self.group_form)
		self.entry_process_priority = QSpinBox(self.group_form)
		self.label_process_insert_order = QLabel("Insertar al final", self.group_form)
		self.entry_process_insert_order = QCheckBox(self.group_form)
		self.entry_process_insert_order.setChecked(True)
		self.button_process_insert = QPushButton('Agregar', self.group_form)
		self.button_process_insert.clicked.connect(lambda: self.insert(self.entry_process_name.text(), self.entry_process_priority.value(), self.entry_process_time.value(), self.entry_process_insert_order.isChecked()))
		self.combobox_algorithm = QComboBox(self.group_form)
		self.combobox_algorithm.addItem("Round Robin")
		self.combobox_algorithm.addItem("SJF")
		self.combobox_algorithm.addItem("FIFO")
		self.combobox_algorithm.addItem("Prioridades")
		self.combobox_algorithm.activated.connect(self.change_algorithm)

		self.layout_group_form.addWidget(self.label_process_name, 0, 0)
		self.layout_group_form.addWidget(self.entry_process_name, 0, 1)
		self.layout_group_form.addWidget(self.label_process_time, 1, 0)
		self.layout_group_form.addWidget(self.entry_process_time, 1, 1)
		self.layout_group_form.addWidget(self.label_process_priority, 2, 0)
		self.layout_group_form.addWidget(self.entry_process_priority, 2, 1)
		self.layout_group_form.addWidget(self.label_process_insert_order, 3, 0)
		self.layout_group_form.addWidget(self.entry_process_insert_order, 3, 1)
		self.layout_group_form.addWidget(self.combobox_algorithm, 4, 0)
		self.layout_group_form.addWidget(self.button_process_insert, 4, 1)

		self.entry_process_time.setMinimum(1)
		self.entry_process_priority.setMinimum(1)

		# Grupo procesos
		self.group_table = QGroupBox("Procesos", self)
		self.layout_group_table = QVBoxLayout(self.group_table)

		self.table = QTableWidget(self.group_table)
		self.table.setColumnCount(3)
		self.table.setHorizontalHeaderLabels(["Nombre", "Prioridad", "Tiempo"])
		self.table.verticalHeader().setVisible(False)
		for column in range(3):
			self.table.horizontalHeader().setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)
		self.button_start = QPushButton('Iniciar', self.group_table)
		self.button_start.clicked.connect(self.start)

		self.layout_group_table.addWidget(self.table)
		self.layout_group_table.addWidget(self.button_start)

		# Agregar al layout principal
		self.layout.addWidget(self.group_form)
		self.layout.addWidget(self.group_table)
		self.w.setLayout(self.layout)

		# Process manager
		self.manager = Manager()
		self.manager.set_algorithm(Algorithm.rr)

		# Table thread
		self.thread_table = ThreadTable(self)
		self.thread_table.signal.connect(self.refresh_table)
		self.thread_table.finished_signal.connect(self.thread_finished)

	def change_algorithm(self):
		self.manager.set_algorithm(Algorithm(self.combobox_algorithm.currentIndex()))
		self.refresh_table()
		print(self.manager.algorithm)

	def start(self):
		if self.thread_table.isRunning():
			self.thread_table.stop = True
			self.button_start.setText('Iniciar')
		else:
			self.thread_table.stop = False
			self.thread_table.start()
			self.button_start.setText('Detener')

	def thread_finished(self):
		self.thread_table.stop = True
		self.button_start.setText('Iniciar')

	def open_file(self):
		file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de Texto (*.txt);;Todos los archivos (*)')
		if file_name:
			self.manager.load_process_from_file(file_name)
			self.refresh_table()

	def insert(self, name: str, priority: int, time: int, end: bool):
			self.manager.push(Process(time, priority, name), end)
			self.refresh_table()

	def refresh_table(self):
		self.table.clearContents()
		self.table.setRowCount(0)

		for i in range(len(self.manager.process)):
			row_pos = self.table.rowCount()
			self.table.insertRow(row_pos)
			self.table.setItem(row_pos, 0, QTableWidgetItem(self.manager.process[i].name))
			self.table.setItem(row_pos, 1, QTableWidgetItem(str(self.manager.process[i].priority)))

			progressBar = QProgressBar()
			progressBar.setValue(self.manager.process[i].time)
			progressBar.setFormat('%v')
			progressBar.setMaximum(20)
			self.table.setCellWidget(row_pos, 2, progressBar)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())