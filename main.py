import sys
import random
import numpy as np

from PyQt5 import QtWidgets, uic
from test import doABarrelRoll
from ui_py.mainwindow import Ui_MainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
 
global data

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.data = []
		self.lineEdit.setText('1000')
		self.lineEdit_3.setText('60')
		self.lineEdit_4.setText('180')
		self.lineEdit_10.setText('10')
		self.lineEdit_2.setText('6')
		self.lineEdit_5.setText('2568')
		self.lineEdit_6.setText('1546')
		self.lineEdit_7.setText('0.7')
		self.lineEdit_8.setText('0.1')
		self.lineEdit_9.setText('0.2')
		self.spinBox.setMinimum(1)

		self.pushButton.clicked.connect(self.justDoIt)
		self.pushButton_1.clicked.connect(self.addmpl)
		self.pushButton_2.clicked.connect(self.addmpl)
		self.pushButton_3.clicked.connect(self.addmpl)
		self.pushButton_4.clicked.connect(self.addmpl)
		self.pushButton_5.clicked.connect(self.addmpl)

	def justDoIt(self):
		N=int(self.lineEdit.text())
		NU_A = int(self.lineEdit_3.text())
		NU_S = int(self.lineEdit_4.text())
		LIMIT = int(self.lineEdit_10.text())
		S_LIMIT = int(self.lineEdit_2.text())
		SEED_A = int(self.lineEdit_5.text())
		SEED_S = int(self.lineEdit_6.text())
		LOOPS = int(self.spinBox.text())
		pP = [1,2,3]
		cP = [float(self.lineEdit_7.text()),float(self.lineEdit_8.text()),float(self.lineEdit_9.text())]
		self.data, processing = doABarrelRoll(N,NU_A,NU_S,LIMIT,S_LIMIT,pP,cP,SEED_A,SEED_S,LOOPS)
		self.label0.setText(str(processing[0]))
		self.label1.setText(str(processing[1]))
		self.label2.setText(str(processing[2]))
		self.label3.setText(str(processing[3]))
		self.label4.setText(str(processing[4]))
		self.label5.setText(str(processing[5]))
		self.label6.setText(str(processing[6]))

	def rmmpl(self,canvas):
		self.mplvl.removeWidget(canvas)
		self.canvas.close()

	def addmpl(self):
		try:
			self.rmmpl(self.canvas)
		except AttributeError:
			pass
		finally:
			sender = self.sender().objectName()
			fig = Figure()
			ax1f1 = fig.add_subplot(111)
			ax1f1.plot(self.data[0],self.data[int(sender[-1])])
			self.canvas = FigureCanvas(fig)
			self.mplvl.addWidget(self.canvas)
			self.canvas.draw()
 
if __name__ == '__main__':
	
	app = QtWidgets.QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	app.exec_()