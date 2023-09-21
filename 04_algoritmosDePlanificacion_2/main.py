import sys
import os
from PyQt6.QtWidgets import *
os.add_dll_directory('C:/mingw64/bin')
from processManager import get_string

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Algoritmos de planificación")
		self.setGeometry(0, 0, 400, 500)

		self.w = QWidget(self)
		self.setCentralWidget(self.w)
		self.layout = QVBoxLayout(self.w)

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
		self.button_process_insert = QPushButton('Agregar', self.group_form)

		self.layout_group_form.addWidget(self.label_process_name, 0, 0)
		self.layout_group_form.addWidget(self.entry_process_name, 0, 1)
		self.layout_group_form.addWidget(self.label_process_time, 1, 0)
		self.layout_group_form.addWidget(self.entry_process_time, 1, 1)
		self.layout_group_form.addWidget(self.label_process_priority, 2, 0)
		self.layout_group_form.addWidget(self.entry_process_priority, 2, 1)
		self.layout_group_form.addWidget(self.label_process_insert_order, 3, 0)
		self.layout_group_form.addWidget(self.entry_process_insert_order, 3, 1)
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

		self.layout_group_table.addWidget(self.table)

		# Agregar al layout principal
		self.layout.addWidget(self.group_form)
		self.layout.addWidget(self.group_table)
		self.w.setLayout(self.layout)

if __name__ == '__main__':

	uwu = get_string()
	for i in uwu:
		print(i)


	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())