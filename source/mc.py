#!/usr/bin/python3
import sys, os, subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QApplication
import glob
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import ntpath
import main
import logging
from imports.zoom import *
from imports.molmass import *
from imports.dialogs import *
from imports.data import *
from imports.calibration import *
import peakutils
import configparser
from imports.readTrc import readTrc
import time as tm
import math as mt

logging.basicConfig(level = logging.DEBUG, format = ' %(asctime)s - %(levelname)s - %(message)s')

class MassCalibration (QtWidgets.QMainWindow, main.Ui_MainWindow):
	about_to_quit = QCoreApplication.aboutToQuit
#initialize everything
	def __init__(self):
		super(MassCalibration, self).__init__()
		self.setupUi(self)
		self.actionNew.triggered.connect(self.New)
		self.actionAbout.triggered.connect(self.about)
		self.actionInstructions.triggered.connect(self.Instruction)
		self.actionLoadProfile.triggered.connect(self.loadCal)
		self.actionSave_profile.triggered.connect(self.saveCal)
		self.actionSave.triggered.connect(self.Save)
		self.actionSave_as.triggered.connect(self.SaveAs)
		self.actionRm_baseline.triggered.connect(self.rmBaseline)
		self.actionUncalibrate.triggered.connect(self.Uncalibrate)
		self.actionCrop.triggered.connect(self.Crop)
		self.btn_removePeaks.clicked.connect(self.clearTable)
		self.btn_saveCal.clicked.connect(self.saveCal)
		self.btn_loadCal.clicked.connect(self.loadCal)
		self.btCalibrate.clicked.connect(self.Calibrate)
		self.actionQuit.triggered.connect(lambda: self.closeEvent(QCloseEvent))
		self.figure = plt.figure()
		self.subplot = self.figure.add_subplot(111) #add a subfigure
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setFocusPolicy(Qt.ClickFocus )
		self.canvas.setFocus()
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.gridLayout_3.addWidget(self.canvas)
		self.gridLayout_3.addWidget(self.toolbar)
		self.figure_1 = plt.figure()
		self.canvas_1 = FigureCanvas(self.figure_1)
		self.toolbar_1 = NavigationToolbar(self.canvas_1, self)
		self.gridLayout_4.addWidget(self.canvas_1)
		self.gridLayout_4.addWidget(self.toolbar_1)
		self.btnAdd.clicked.connect(self.addFiles)
		self.btnClear.clicked.connect(self.listClear)
		self.btnPlot.clicked.connect(self.plotDecay)
		self.pushButton_2.clicked.connect(self.menuUpClicked)
		self.pushButton.clicked.connect(self.menuDownClicked)
		self.pushButton_3.clicked.connect(self.menuRemoveClicked)
		self.btnPlot.setEnabled(False)
		self.btnPlot.setDisabled(True)
		self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.listWidget.itemClicked.connect(self.listItemRightClicked)
		self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget.customContextMenuRequested.connect(self.tableItemRightClicked)
		self.tableWidget.cellChanged.connect(self.cellchanged)
		self.canvas.mpl_connect('button_press_event', self.onclick)
		self.config = self.ReadConfig()
		self.fname = ''
		self.lastDrawn=0
		self.data = Data()
		self.Calibration =Calibration()
		self.label_2.setText("")
		self.scatter = 0
		self.p1 = True
		self.p2 = False
		self.GaussFit= True
		self.save2col = False
		self.files=[]
		self.decay=[]
		self.dwTime = -1
		self.scale = 1.5
		self.zp = ZoomPan()
		figZoom = self.zp.zoom_factory(self.subplot, base_scale = self.scale)
		figPan = self.zp.pan_factory(self.subplot)
		self.fontSize = int(self.config['DEFAULT']['fontSize'])
		matplotlib.rcParams.update({'font.size': self.fontSize})
		self.New()

	def closeEvent(self,event):
		result = QMessageBox.question(self,
			"Confirm Exit...",
			"Are you sure you want to exit ?",
			QMessageBox.Yes| QMessageBox.No)
		event.ignore()

		if result == QMessageBox.Yes:
			QApplication.exit()

	def ReadConfig(self):
		config = configparser.ConfigParser()
		try:
			config.read(os.path.expanduser('~')+'/.config/masscalibration/config.ini')
		except:
			config.read(os.path.dirname(sys.argv[0]) +'/config/config.ini')
		self.h=int(config['DEFAULT']['header'])
		self.initialDir=config['DEFAULT']['path']
		self.yCol=int(config['DEFAULT']['y'])
		self.xCol=int(config['DEFAULT']['x'])
		self.inversed=bool(config['DEFAULT']['inversed'])
		return config

	def rmBaseline(self):
		baseline = peakutils.baseline(self.data.Y)
		self.subplot.plot(self.data.X, baseline, 'r--')
		self.canvas.draw()
		reply = QMessageBox.question(self, 'Remove baseline?', 'Do you want to remove the baseline?', QMessageBox.Yes, QMessageBox.No)
		self.Plot()

	def ImportDiag(self):
		dialog = ImportDialog(self.config)
		result = dialog.exec_()
		param = 0
		param = dialog.getData()
		if result == QtWidgets.QDialog.Accepted:
			print ("Nr. of columns: %d\nXcolumn: %d\nYcolumn: %d\ndelimiter: %s\nInverse?: %s" %(int(param[0]), int(param[1]), int(param[2]), param[3], param[4]))
			return param

	def SaveDiag(self):
		dialog = SaveDialog()
		result = dialog.exec_()
		param = 0
		param = dialog.getData()
		print(result)
		if result == QtWidgets.QDialog.Accepted:
			print ("Delimiter: %s\nTwo columns: %s" %(param[0], param[1]))
			return param

	def addFiles(self):
		path = self.initialDir
		files, _filter = QtWidgets.QFileDialog.getOpenFileNames(self, 'Load files', path,"Binnary files (*.trc);; Text files (*.txt *.dat);; All files (*.*)")
		self.initialDir=ntpath.dirname(files[0]) #update the initial directory for the Open/Save dialog
		self.files = np.sort(np.append(self.files, files))
		self.listWidget.clear()
		for file_ in self.files:
			item = QListWidgetItem(ntpath.basename(file_))
			self.listWidget.addItem(item)

	def listItemRightClicked(self, QPos):
		self.listMenu= QMenu()
		menu_item_1 = self.listMenu.addAction("Plot Spectrum")
		menu_item_2 = self.listMenu.addAction("Move Up")
		menu_item_3 = self.listMenu.addAction("Move Down")
		menu_item = self.listMenu.addAction("Remove Item")
		menu_item.triggered.connect(self.menuRemoveClicked)
		menu_item_1.triggered.connect(self.menuPlotClicked)
		menu_item_2.triggered.connect(self.menuUpClicked)
		menu_item_3.triggered.connect(self.menuDownClicked)
		parentPosition = self.listWidget.mapToGlobal(QPoint(0, 0))
		self.listMenu.move(parentPosition + QPos)
		self.listMenu.show()

	def menuRemoveClicked(self):
		currentItemName=str(self.listWidget.currentItem().text() )
		self.listWidget.takeItem(self.listWidget.currentRow())
		self.files = np.delete(self.files, self.listWidget.currentRow())
		if self.listWidget.count()==0:
			self.btnPlot.setEnabled(False)
			self.decay=[]

	def menuUpClicked(self):
		index = self.listWidget.currentRow()
		if index>0:
			temp = self.files[index]
			self.files[index]=self.files[index-1]
			self.files[index-1]=temp
			self.listWidget.clear()
			for file_ in self.files:
				item = QListWidgetItem(ntpath.basename(file_))
				self.listWidget.addItem(item)
			self.listWidget.setCurrentRow(index-1)

	def menuDownClicked(self):
		index = self.listWidget.currentRow()
		if index<len(self.files)+1:
			temp = self.files[index]
			self.files[index]=self.files[index+1]
			self.files[index+1]=temp
			self.listWidget.clear()
			for file_ in self.files:
				item = QListWidgetItem(ntpath.basename(file_))
				self.listWidget.addItem(item)
			self.listWidget.setCurrentRow(index+1)

	def listClear(self):
		self.figure_1.clf()	#clear the figure
		self.canvas_1.draw() #draw everything to the screen
		self.files=[]
		self.decay=[]
		self.listWidget.clear()
		self.btnPlot.setEnabled(False)

	def menuPlotClicked(self):
		x, y, d = readTrc(self.files[self.listWidget.currentRow()])
		baseline= peakutils.baseline(abs(y))
		y = 1000*(y - baseline)
		x = x*1000
		self.figure_1.clf()	#clear the figure
		self.subplot_1 = self.figure_1.add_subplot(111) #add a subfigure
		self.subplot_1.plot(x, y)
		self.subplot_1.set_xlabel('time of flight, ms', fontsize = self.fontSize) #uncalibrated data
		self.subplot_1.set_ylabel('Intensity, mV', fontsize = self.fontSize)
		self.subplot_1.set_xlim([x[0], x[-1]]) #X axis limits
		self.subplot_1.set_ylim([min(y), 1.1*max(y)])
		self.figure_1.subplots_adjust(left=0.085, bottom=0.08, top=0.955, right=0.995) #reduce margins
		self.subplot_1.set_title(self.listWidget.currentItem().text())
		self.canvas_1.draw() #draw everything to the screen
		self.btnPlot.setEnabled(True)

	def plotDecay(self):
		center = np.mean(self.subplot_1.get_xlim())
		width = self.subplot_1.get_xlim()[1]-self.subplot_1.get_xlim()[0]
		print("center: %.4f\nwidth: %.4f" %(center, width))
		i=1
		nFiles = len(self.files)
		self.progressBar.setValue(0)
		out=[[0,0]]
		for item in self.files:
			x, y, d = readTrc(item)
			baseline= peakutils.baseline(abs(y))
			y = 1000*(y - baseline)
			x = x*1000
			zero = np.argwhere(x>0)[0]
			start = np.where(x > (center - width / 2.0))[0]
			stop = np.where(x > (center + width / 2.0))[0]
			temp = y[start[0]: stop[0]]
			tp = np.trapz(temp) #integral
			#tp = np.amax(temp) #intensity
			des = int(ntpath.basename(item)[-7: -4])
			out= np.append(out, [[i, tp]], axis=0)
			print("file %s processed" % item)
			self.progressBar.setValue(int(i*100/nFiles))
			i = i+1
		self.decay = np.delete(out, 0, axis=0)
		np.savetxt(self.initialDir+'/out.dat', self.decay, delimiter=' ')
		print("output saved")
		self.figure_1.clf()	#clear the figure
		self.subplot_1 = self.figure_1.add_subplot(111) #add a subfigure
		self.subplot_1.scatter(self.decay[:,0], self.decay[:,1])
		self.subplot_1.set_xlabel('nr of shots', fontsize = self.fontSize)
		self.subplot_1.set_ylabel('Intensity, V s', fontsize = self.fontSize)
		self.subplot_1.set_ylim(ymin=0)
		self.subplot_1.set_title('Decay curve')
		self.progressBar.setValue(0)
		self.figure_1.savefig(self.initialDir+'/decay_fig.png')
		print('figure saved')
		self.canvas_1.draw() #draw everything to the screen


	def Crop(self):
		if self.Calibration.calibrated:
			_min = self.data.M[0]
			_max = self.data.M[-1]
		else:
			_min = self.data.X[0]
			_max = self.data.X[-1]
		dialog = CropDialog(_min, _max)
		result = dialog.exec_()
		params = dialog.getData()
		if result == QtWidgets.QDialog.Accepted:
			try:
				_min = int(params[0])
				_max = int(params[1])
				print(_min, _max)
				self.data.crop(_min, _max, self.Calibration.calibrated)
				self.Plot()
			except ValueError:
				self.showWarning("Non valid data", "Only numbers are allowed")

	def Uncalibrate(self):
		if (self.Calibration.calibrated):
			self.Calibration.calibrated = False
			self.label_2.setText("")
			self.Plot()


	def Calibrate(self):
		if (self.Calibration.calibrated):
			self.Calibration.calibrated = False
		if (self.checkMasses()):
			self.coef = np.asarray(['%.5g'%n for n in self.Calibration.calibrate()])
			if not self.coef[1][0]=='-':
				self.coef[1] = "+"+self.coef[1]
			if not self.coef[2][0]=='-':
				self.coef[2] = "+"+self.coef[2]
			self.label_2.setText("f(t) =%s*t<sup>2</sup>%s*t%s" %(self.coef[0], self.coef[1], self.coef[2]))
			self.data.M = self.Calibration.calibration(self.data.X)
			error = self.Calibration.calcError()
			for i in np.arange(0, len(error)):
				self.tableWidget.item(i, 3).setText("%.4f"%error[i])
		self.Plot()  #plot spectrum

#load calibration file
	def loadCal(self):
		path = self.initialDir
		fname, _filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Load calibration profile', path,"Calibration (*.mz);; Text files (*.txt *.dat);; All files (*.*)")
		if not fname:
			return
		else:
			try:
				with open(fname) as f:
					for i, line in enumerate(f):
						if i==2:
							par = line
				if par[0]=='#':
					par = par[1:]
				calibr = np.fromstring(par, dtype=float, sep=',')
				print(calibr)
				self.clearTable()
				self.Calibration.setCalibration(calibr)
				self.coef = np.asarray(['%.5g'%n for n in calibr])
				if not self.coef[1][0]=='-':
					self.coef[1] = "+"+self.coef[1]
				if not self.coef[2][0]=='-':
					self.coef[2] = "+"+self.coef[2]
				self.label_2.setText("f(t) =%s*t<sup>2</sup>%s*t%s" %(self.coef[0], self.coef[1], self.coef[2]))

				temp = np.loadtxt(fname, delimiter=',', dtype = np.str)
				for i, time in enumerate(temp[:,0]):
					pos, intens, error = self.findPeak(self.data, float(time), False)
					self.Calibration.addPeak([pos, intens, float(temp[i,2]), temp[i,3]])
					rowPosition = self.tableWidget.rowCount()
					self.tableWidget.insertRow(rowPosition)
					self.tableWidget.setItem(rowPosition , 0, QTableWidgetItem("%.6f" % pos))
					self.tableWidget.setItem(rowPosition , 1, QTableWidgetItem(temp[i,2]))
					self.tableWidget.setItem(rowPosition , 2, QTableWidgetItem(temp[i,3]))
					self.tableWidget.setItem(rowPosition , 3, QTableWidgetItem("--"))
				self.relocatePeaks()
				self.plotPeaks()
			except IOError:
				self.showWarning('Error', 'Could not read the file')

#save calibration profile
	def saveCal(self):
		if not self.Calibration.calibrated:
			self.showWarning("Not calibrated!", "Please calibrate first")
			return
		path = self.initialDir
		name, _filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save calibration profile', path, "Calibration (*.mz);; All files (*.*)")
		if not name:
			return
		else:
			if name[-3:]!='.mz':
				name = name+'.mz'
			text = "Calibration coefficients\nhighest to lower power\n%.6g, %.6g, %.6g\n\nTime, Intensity, Mass, Formula" %(self.Calibration.coef[0], self.Calibration.coef[1], self.Calibration.coef[2])
			np.savetxt(name, self.Calibration.peaks.values, header = text,fmt='%.4f,  %.1f, %.4f, %s')
			print("Calibration profile saved")

#new file
	def New( self):
		# open file dialog
		path = self.initialDir
		fname, _filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', path,"Text files (*.txt *.dat);; NPZ files (*.npz *.mc);; Binnary files (*.trc);; All files (*.*)")
		if not fname:
			return
		else:
			self.initialDir=ntpath.dirname(fname) #update the initial directory for the Open/Save dialog
			if fname[-3:]=='trc': #read the binary file
				print("trc file")
				try:
					x, y, d = readTrc(fname)
					DataIn = np.column_stack((x, y))
				except IOError:
					self.showWarning('Error', 'Could not read the file')
					return
			elif fname[-3:]=='npz': #read the npz file
				print("npz file")
				try:
					dt = np.load(fname)
					DataIn = dt['a']
				except IOError:
					self.showWarning('Error', 'Could not read the file')
					return
			else:
				params = self.ImportDiag() #display dialog for import options
				if np.shape(params):
					if int(params[1])+1>int(params[0]) or int(params[2])+1>int(params[0]) :
						self.showWarning("Error", "bad column values")
						return
					else:
						self.xCol= int(params[1])
						self.yCol= int(params[2])
						self.inversed = self.str2bool(params[4])
				else:
					return
				try:
					DataIn = np.loadtxt(fname, skiprows=self.h, usecols=range(int(params[0])), delimiter=params[3]) #read a text file
				except IOError :
					self.showWarning('Error', 'Could not read the file')
					return
				except IndexError:
					self.showWarning('Error', 'Wrong delimiter')
					return
				except ValueError:
					self.showWarning('Error', 'Wrong nr of columns')
					return
			self.fname = fname
			self.setWindowTitle( ntpath.basename(fname)+ ' - Mass Spectrum Calibration - v2.001')
			self.data.setData(DataIn[:, self.xCol], DataIn[:, self.yCol])

		self.lastDrawn = 0
		self.Calibration.calibrated = False
		v1 = False
		v2 = False
		if len(self.Calibration.peaks['mass']):
			self.relocatePeaks()
		#draw everything
		self.Plot()  #plot time-of-flight spectrum

	def str2bool(self, v):
		return v.lower() in ("yes", "true", "t", "1")

#save file
	def Save(self):
		path = self.initialDir
		if self.tabWidget.currentIndex()==1:
			if self.decay!=[]:
				name, _filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', self.fname, "Text files (*.txt);; Data files (*.dat);; All files (*.*)")
				if not name:
					return
				else:
					np.savetxt(name, self.decay,header="Signal decay", delimiter='	')
					print("file saved")
		else:
			if not self.Calibration.calibrated:
				self.showWarning("Error", "No calibration have been applied\nFirst calibrate your data")
				return
			name, _filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', self.fname, "Text files (*.txt);; Data files (*.dat);; All files (*.*)")
			if not name:
				return
			else:
				params = self.SaveDiag()
				if np.shape(params):
					self.save2col = self.str2bool(params[1])
				else:
					return
				if self.save2col:
					if self.inversed:
						np.savetxt(name, np.transpose([self.data.M, self.data.max-self.data.Y[self.data.zero:]]), delimiter=params[0])
					else:
						np.savetxt(name, np.transpose([self.data.M, self.data.Y[self.data.zero:]]), delimiter=params[0])
				else:
					header="Calibrated Mass Spectrum\nCalibration coefficients:\n%s, %s, %s\ntime	mass	signal" % (self.coef[0], self.coef[1], self.coef[2])
					if self.inversed:
						np.savetxt(name, np.transpose([self.data.X[self.data.zero:],self.data.M, self.data.max-self.data.Y[self.data.zero:]]), header = header, delimiter=params[0])
					else:
						np.savetxt(name, np.transpose([self.data.X[self.data.zero:],self.data.M, self.data.Y[self.data.zero:]]), header = header, delimiter=params[0])
				print("file saved")

	def SaveAs(self):
		if not self.Calibration.calibrated:
			self.showWarning("Error", "No calibration have been applied\nFirst calibrate your data")
			return
		path = self.initialDir
		name, _filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', path, "NPZ files (*.npz);; All files (*.*)")
		if not name:
			return
		else:
			if self.save2col:
				if self.inversed:
					np.savez_compressed(name, a=np.transpose([self.data.M, self.data.max-self.data.Y[self.data.zero:]]))
				else:
					np.savez_compressed(name, a=np.transpose([self.data.M, self.data.Y[self.data.zero:]]))
			else:
				if self.inversed:
					np.savez_compressed(name, a=np.transpose([self.data.X[self.data.zero:],self.data.M, self.data.max-self.data.Y[self.data.zero:]]))
				else:
					np.savez_compressed(name, a=np.transpose([self.data.X[self.data.zero:],self.data.M, self.data.Y[self.data.zero:]]))
			print("file saved")

#warning pop-up message
	def showWarning(self, title, message):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText(message)
		msg.setWindowTitle(title)
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

#information pop-up message
	def about(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Version v2.2 Beta\nMade by CAT\nLille, 2018")
		msg.setWindowTitle("About")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

	def Instruction(self):
		filepath = 'README.md'
		if sys.platform.startswith('darwin'):
			subprocess.call(('open', filepath))
		elif os.name == 'nt': # For Windows
			os.startfile(filepath)
		elif os.name == 'posix': # For Linux, Mac, etc.
			subprocess.call(('xdg-open', filepath))

#Plot the data
	def Plot(self):
		#self.figure.clf()	#clear the figure
		#self.subplot = self.figure.add_subplot(111) #add a subfigure
		self.subplot.clear()
		if self.Calibration.calibrated:
			if self.inversed:	#plot the inversed data
				self.subplot.plot(self.data.M , self.data.max-self.data.Y[self.data.zero:])
				self.subplot.set_ylim([0.9*self.data.max,  self.data.max-self.data.min])
			else:
				self.subplot.plot(self.data.M , self.data.Y[self.data.zero:])
				self.subplot.set_ylim([self.data.min, 1.1 * self.data.max])

			self.subplot.set_xlim([self.data.M[0],500])#self.data.M[-1]]) #X axis limits
			self.subplot.set_ylabel('Intensity', fontsize = self.fontSize)
			self.subplot.set_xlabel('m/z', fontsize = self.fontSize) #calibrated data

		else:
			if self.inversed:	#plot the inversed data
				self.subplot.plot(self.data.X , self.data.max-self.data.Y)
				self.subplot.set_ylim([0.9*self.data.max,  self.data.max-self.data.min])
			else:
				self.subplot.plot(self.data.X , self.data.Y)
				self.subplot.set_ylim([self.data.min, 1.1 * self.data.max])
			self.subplot.set_xlim([self.data.X[0],self.data.X[self.data.len-1]]) #X axis limits
			self.subplot.set_ylabel('Intensity', fontsize = self.fontSize)
			self.subplot.set_xlabel('time of flight', fontsize = self.fontSize) #uncalibrated data
		self.scatter = 0
		self.plotPeaks()
		self.canvas.draw() #draw everything to the screen
		self.figure.tight_layout()


	def plotPeaks(self):
		self.removeScatter()
		if (self.Calibration.peaks['mass'].shape):
			if (self.Calibration.calibrated):
				self.scatter = self.subplot.scatter(self.Calibration.peaks['mass'], self.Calibration.peaks['intensity'], s =70, facecolors='r', marker='v')
			else:
				self.scatter = self.subplot.scatter(self.Calibration.peaks['time'], self.Calibration.peaks['intensity'], s =70, facecolors='r', marker='v')
			self.canvas.draw()

	def removeScatter(self):
		if(self.scatter):
			self.scatter.remove()
			self.scatter=0
			self.canvas.draw()

	def menuPeak(self,x, Gfit):
		mass = -1
		text = '--'
		if self.Calibration.calibrated:
			mass = x
			x = np.interp(mass, self.data.M, self.data.X)
			text = str(mass)
		pos, intens, error = self.findPeak(self.data, x, Gfit)
		self.Calibration.addPeak([pos, intens, mass, '--'])
		rowPosition = self.tableWidget.rowCount()
		self.plotPeaks()
		self.tableWidget.insertRow(rowPosition)
		self.tableWidget.setItem(rowPosition , 0, QTableWidgetItem("%.6f" % pos))
		self.tableWidget.setItem(rowPosition , 1, QTableWidgetItem(text))
		self.tableWidget.setItem(rowPosition , 2, QTableWidgetItem("--"))
		self.tableWidget.setItem(rowPosition , 3, QTableWidgetItem("--"))

	def tableItemRightClicked(self, QPos):
		self.listMenu= QtWidgets.QMenu()
		menu_item_1 = self.listMenu.addAction("Remove")
		menu_item_1.triggered.connect( self.menuRemoveRow)
		parentPosition = self.tableWidget.mapToGlobal(QPoint(0, 0))
		self.listMenu.move(parentPosition + QPos)
		self.listMenu.show()

	def clearTable(self):
		if self.Calibration.calibrated:
			self.Uncalibrate()
		self.Calibration.clear()
		while self.tableWidget.rowCount()!=0:
			self.tableWidget.removeRow(0)
		self.removeScatter()

	def checkMasses(self):
		if len(self.Calibration.peaks['mass'].values)==0:
			self.showWarning("No calibration data", "Please add calibration peaks")
			return False
		if -1 in self.Calibration.peaks['mass'].values:
			return False
		else:
			return True

	def menuRemoveRow(self):
		index = self.tableWidget.currentRow()
		print(index)
		self.tableWidget.removeRow(index)
		self.Calibration.removePeak(index)
		if (self.scatter):
			self.scatter.remove()
		if (self.Calibration.calibrated):
			self.scatter = self.subplot.scatter(self.Calibration.peaks['mass'], self.Calibration.peaks['intensity'], s =70, facecolors='r', marker='v')
		else:
			self.scatter = self.subplot.scatter(self.Calibration.peaks['time'], self.Calibration.peaks['intensity'], s =70, facecolors='r', marker='v')
		self.canvas.draw()


	def cellchanged(self):
		col = self.tableWidget.currentColumn()
		if col ==1:
			try:
				mass= float(self.tableWidget.currentItem().text())
				self.tableWidget.currentItem().setBackground(self.tableWidget.item(0,0).background())
				self.Calibration.setMass(self.tableWidget.currentRow(), [mass, '--'])
			except ValueError:
				self.tableWidget.currentItem().setBackground(QColor(255,0,0))
			self.tableWidget.clearSelection()
		elif col ==2:
			try:
				mass= Formula(self.tableWidget.currentItem().text()).isotope.mass
				self.tableWidget.currentItem().setBackground(self.tableWidget.item(0,0).background())
				self.tableWidget.item(self.tableWidget.currentRow(), 1).setText("%.4f"%mass)
				self.Calibration.setMass(self.tableWidget.currentRow(), [mass, self.tableWidget.currentItem().text()])
			except FormulaError:
				self.tableWidget.currentItem().setBackground(QColor(255,0,0))
			self.tableWidget.clearSelection()

	def relocatePeaks (self):
		print(self.Calibration.peaks['time'])
		for i in np.arange(0, len(self.Calibration.peaks['time'])):
			pos, intens, error = self.findPeak(self.data, self.Calibration.peaks['time'][i], True)
			print('Error: ', error)
			if not error:
				self.Calibration.peaks['time'][i] = pos
				self.Calibration.peaks['intensity'][i] = intens
				self.tableWidget.item(i, 0).setText("%.6f"%pos)
				self.tableWidget.item(i, 0).setBackground(self.tableWidget.item(0,3).background())
			else:
				self.tableWidget.item(i,0).setBackground(QColor(255,0,0))
			self.tableWidget.clearSelection()
		self.plotPeaks()


	def findPeak(self, data, x, Gfit ):
		print('Gfit = ', Gfit)
		self.min = data.min
		self.max = data.max
		width=70
		Xpos = x
		ind=(np.abs(data.X-Xpos)).argmin()
		Ypos = data.Y[ind]
		error = 0
		if Gfit:
			try:
				#Xpos = peakutils.gaussian_fit(data.X[ind-width: ind+width], data.Y[ind-width:ind+width], center_only=True )
				dt=data.Y[ind-width: ind+width]
				Ypos = max(data.Y[ind-width+peakutils.indexes(dt,thres = 0.02/max(dt), min_dist =100)])
				Xpos = data.X[data.Y ==Ypos][0]
				logging.info("New pos %f" % Xpos)
			except RuntimeError:
				print("Failed to fit a gaussian")
				error = 1
		#if (self.dwTime>(-1)):
			#self.subplot.lines.remove(self.cursor)
		self.dwTime = tm.time()
		#self.cursor, = self.subplot.plot([Xpos, Xpos], [self.min, self.max], 'r', gid = self.dwTime)
		return Xpos, Ypos, error

#right click on the plot
	def onclick(self, event):
		if event.button == 3:  #right click
			self.listMenu= QtWidgets.QMenu()
			menu_item_0 = self.listMenu.addAction("Use the gaussian fit")
			menu_item_1 = self.listMenu.addAction("Use the cursor data")
			print("position:\nx=%f\ny=%f" %(event.xdata, event.ydata))
			menu_item_0.triggered.connect( lambda: self.menuPeak(event.xdata, True))
			menu_item_1.triggered.connect( lambda: self.menuPeak(event.xdata, False))
			parentPosition = self.listWidget.mapToGlobal(QPoint(0, 0))
			cursor = QCursor()
			self.listMenu.move(cursor.pos() )
			self.listMenu.show()

	def cleanUp(self):
		print('closing')

app = None

def main():
	global app
	app = QApplication(sys.argv)

	form = MassCalibration()
	form.show()
	app.aboutToQuit.connect(lambda: form.cleanUp)
	print('and here')
	app.exec()


if __name__ == '__main__':
	main()
