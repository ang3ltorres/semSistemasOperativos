import sys
import random
import time
import threading

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

LOCKED = False

class RW():
	def __init__(self, writer: bool, mainWindow):
		self.mainWindow = mainWindow

		self.active = False
		self.error = False
		self.writer = writer
		self.value = 0
		self.set_timer()

	def set_timer(self):
		if self.writer:
			self.timer = random.choice([0.5, 1, 2])
		else:
			self.timer = random.choice([1, 1.5, 2])

	def thread(self):
		global LOCKED

		while (True):

			if (self.timer > 0):
				self.timer -= 0.1
				self.mainWindow.reader_writer.update()
				time.sleep(0.1)

			elif not LOCKED:
				self.active = True
				self.error = False
				self.mainWindow.reader_writer.update()

				if (self.writer):
					self.write()
				else:
					self.read()				
			else:
				self.error = True
				self.mainWindow.reader_writer.update()
				self.set_timer()

	def read(self):
		file = open('file.txt', 'r')
		self.value = int(file.readline())
		file.close()

		time.sleep(1)
		self.set_timer()
		self.active = False
		self.mainWindow.reader_writer.update()

	def write(self):
		global LOCKED
		LOCKED = True

		file = open('file.txt', 'r+')
		self.value = int(file.readline())
		self.value += 1
		file.seek(0)
		file.write(str(self.value))
		file.close()

		time.sleep(1)
		self.set_timer()
		self.active = False
		self.mainWindow.reader_writer.update()
		
		LOCKED = False

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('Lector - Escritor 1')

		self.w = QWidget(self)
		self.setCentralWidget(self.w)

		self.group_reader_writer = QGroupBox('Representación visual', self)
		self.layout_group_reader_writer = QVBoxLayout(self.group_reader_writer)
		self.reader_writer = ReaderWriter(self.group_reader_writer, self)
		self.layout_group_reader_writer.addWidget(self.reader_writer)

		### LAYOUT PRINCIPAL ###
		self.layout = QVBoxLayout(self.w)
		self.layout.addWidget(self.group_reader_writer)
		self.w.setLayout(self.layout)

		### HILOS ###
		self.r1 = RW(False, self)
		thread_r1 = threading.Thread(target=self.r1.thread)
		thread_r1.daemon = True
		thread_r1.start()

		self.r2 = RW(False, self)
		thread_r2 = threading.Thread(target=self.r2.thread)
		thread_r2.daemon = True
		thread_r2.start()

		self.w1 = RW(True, self)
		thread_w1 = threading.Thread(target=self.w1.thread)
		thread_w1.daemon = True
		thread_w1.start()

		self.w2 = RW(True, self)
		thread_w2 = threading.Thread(target=self.w2.thread)
		thread_w2.daemon = True
		thread_w2.start()

class ReaderWriter(QWidget):
	def __init__(self, parent, mainWindow: MainWindow):
		super().__init__(parent)
		self.mainWindow = mainWindow
		self.setMinimumSize(800, 600)
		self.setMaximumSize(800, 600)

		self.font = QFont('Consolas', 12)
		self.pen = QPen(QColorConstants.Black, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap)

		self.painter = QPainter()

	def paintEvent(self, event):
		self.painter.begin(self)
		self.painter.setFont(self.font)
		self.painter.setPen(self.pen)

		self.painter.fillRect(self.rect(), Qt.GlobalColor.white)

		#
		self.painter.fillRect(300, 200, 25, 25, Qt.GlobalColor.blue)
		self.painter.fillRect(300, 230, 25, 25, Qt.GlobalColor.green)
		self.painter.fillRect(300, 260, 25, 25, Qt.GlobalColor.gray)
		self.painter.fillRect(300, 290, 25, 25, Qt.GlobalColor.red)

		self.painter.drawText(300+30, 200+12, 'Escribiendo')
		self.painter.drawText(300+30, 230+12, 'Leyendo')
		self.painter.drawText(300+30, 260+12, 'Inactivo')
		self.painter.drawText(300+30, 290+12, 'Error')

		# LECTOR 1
		self.painter.fillRect(0, 0, 100, 100, self.getColor(self.mainWindow.r1))
		self.painter.drawText(100, 12, 'LECTOR 1')
		self.painter.drawText(0, 12, str(self.mainWindow.r1.value))
		self.painter.drawText(0, 24, str(round(abs(self.mainWindow.r1.timer), 1)))
		
		# LECTOR 2
		self.painter.fillRect(0, 600-100, 100, 100, self.getColor(self.mainWindow.r2))
		self.painter.drawText(100, 600-4, 'LECTOR 2')
		self.painter.drawText(0, 600-4, str(self.mainWindow.r2.value))
		self.painter.drawText(0, 600-4-12, str(round(abs(self.mainWindow.r2.timer), 1)))

		# ESCRITOR 1
		self.painter.fillRect(800-100, 0, 100, 100, self.getColor(self.mainWindow.w1))
		self.painter.drawText(800-120-70, 12, 'ESCRITOR 1')
		self.painter.drawText(750, 12, str(self.mainWindow.w1.value))
		self.painter.drawText(750, 24, str(round(abs(self.mainWindow.w1.timer), 1)))

		# ESCRITOR 2
		self.painter.fillRect(800-100, 600-100, 100, 100, self.getColor(self.mainWindow.w2))
		self.painter.drawText(800-120-70, 600-4, 'ESCRITOR 2')
		self.painter.drawText(750, 600-4, str(self.mainWindow.w2.value))
		self.painter.drawText(750, 600-4-12, str(round(abs(self.mainWindow.w2.timer), 1)))

		self.painter.end()

	def getColor(self, rw: RW) -> QColor:
		if (rw.error):
			return Qt.GlobalColor.red
		elif (rw.active):
			if (rw.writer):
				return Qt.GlobalColor.blue
			else:
				return Qt.GlobalColor.green
		else:
			return Qt.GlobalColor.gray

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
