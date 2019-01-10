#!/usr/bin/python3
import glob
import matplotlib
matplotlib.use('Qt5Agg')
import sys, os, subprocess
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import ntpath
import main
import logging
import logging.config
import peakutils
import configparser
import time as tm
import math as mt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QApplication, QListWidget, QListWidgetItem, QAction
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from imports.zoom import *
from imports.molmass import *
from imports.dialogs import *
from imports.data import *
from imports.calibration import *
from imports.readTrc import readTrc


class MassCalibration (QtWidgets.QMainWindow, main.Ui_MainWindow):
	about_to_quit = QCoreApplication.aboutToQuit
	resized = pyqtSignal()
	logging.config.fileConfig('logs/log.ini')

#initialize everything
	def __init__(self):
		super(MassCalibration, self).__init__()
		self.setupUi(self)
		#toolbar
		self.tb = self.addToolBar("File")
		new = QAction(QIcon("designs/new.png"),"New",self)
		save = QAction(QIcon("designs/save.png"),"Save",self)
		saveAs = QAction(QIcon("designs/saveAs.png"),"Save as npz",self)
		crop = QAction(QIcon("designs/crop.png"),"Crop",self)
		baseline = QAction(QIcon("designs/baseline.png"),"Remove baseline",self)
		loadCal = QAction(QIcon("designs/open.png"),"Load calibration",self)
		saveCal = QAction(QIcon("designs/export.png"),"Save calibration",self)
		cal = QAction(QIcon("designs/plot.png"),"Calibrate",self)
		cal_formula = QAction(QIcon("designs/plot_math.png"),"Calibrate (formula)",self)
		uncal = QAction(QIcon("designs/plot_remove.png"),"Uncalibrate",self)
		self.tb.addAction(new)
		self.tb.addAction(save)
		self.tb.addAction(saveAs)
		self.tb.addSeparator()
		self.tb.addAction(crop)
		self.tb.addAction(baseline)
		self.tb.addSeparator()
		self.tb.addAction(loadCal)
		self.tb.addAction(saveCal)
		self.tb.addAction(cal)
		self.tb.addAction(cal_formula)
		self.tb.addAction(uncal)
		self.tb.addSeparator()
		new.triggered.connect(self.New)
		save.triggered.connect(self.Save)
		saveAs.triggered.connect(self.SaveAs)
		crop.triggered.connect(self.Crop)
		baseline.triggered.connect(self.rmBaseline)
		loadCal.triggered.connect(self.loadCal)
		saveCal.triggered.connect(self.saveCal)
		cal.triggered.connect(self.Calibrate)
		cal_formula.triggered.connect(self.CalibrateFormula)
		uncal.triggered.connect(self.Uncalibrate)
		self.tb.toggleViewAction().setChecked(True)

		#connect to UI
		self.actionNew.triggered.connect(self.New)
		self.actionAbout.triggered.connect(self.about)
		self.actionInstructions.triggered.connect(self.Instruction)
		self.actionLoadProfile.triggered.connect(self.loadCal)
		self.actionSaveProfile.triggered.connect(self.saveCal)
		self.actionSave.triggered.connect(self.Save)
		self.actionSave_as.triggered.connect(self.SaveAs)
		self.actionRm_baseline.triggered.connect(self.rmBaseline)
		self.actionUncalibrate.triggered.connect(self.Uncalibrate)
		self.actionCrop.triggered.connect(self.Crop)
		self.actionCalibrate_formula.triggered.connect(self.CalibrateFormula)
		self.actionQuit.triggered.connect(lambda: self.closeEvent(QCloseEvent))
		self.actionCalibrate.triggered.connect(self.Calibrate)
		self.actionReloadConfig.triggered.connect(self.ReloadConfig)
		self.actionShow_toolbar.triggered.connect(self.tb.toggleViewAction().trigger)

		self.btnAdd.clicked.connect(self.addFiles)
		self.btnClear.clicked.connect(self.listClear)
		self.btnPlot.clicked.connect(self.plotDecay)
		self.pushButton_2.clicked.connect(self.menuUpClicked)
		self.pushButton.clicked.connect(self.menuDownClicked)
		self.pushButton_3.clicked.connect(self.menuRemoveClicked)
		self.btnPlot.setEnabled(False)
		self.btnPlot.setDisabled(True)

		self.resized.connect(self.onResize)

		self.scale = 1.5
		self.config = self.ReadConfig()
		self.setTheme()
		self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget.customContextMenuRequested.connect(self.tableItemRightClicked)
		self.listWidget.itemClicked.connect(self.listItemRightClicked)
		self.tableWidget.cellChanged.connect(self.cellchanged)
		self.fname = ''
		self.lastDrawn=0
		self.data = Data()
		self.Calibration =Calibration()
		self.label_2.setText("")
		self.scatter = 0
		self.p1 = True
		self.p2 = False
		self.save2col = False
		self.files=[]
		self.decay=[]
		self.dwTime = -1
		self.fontSize = int(self.config['DEFAULT']['fontSize'])
		matplotlib.rcParams.update({'font.size': self.fontSize})
		self.New()

	def setTheme (self):
		#calibration
		self.figure = plt.figure(edgecolor=self.fg_col, facecolor=self.bg_col)
		self.subplot = self.figure.add_subplot(111,facecolor=self.bg_col) #add a subfigure
		self.subplot.spines['bottom'].set_color(self.fg_col)
		self.subplot.spines['left'].set_color(self.fg_col)
		self.subplot.patch.set_facecolor(self.bg_col)
		self.subplot.xaxis.set_tick_params(color=self.fg_col, labelcolor=self.fg_col)
		self.subplot.yaxis.set_tick_params(color=self.fg_col, labelcolor=self.fg_col)
		#decay
		self.figure_1 = plt.figure(edgecolor=self.fg_col, facecolor=self.bg_col)
		self.subplot_1 = self.figure_1.add_subplot(111,facecolor=self.bg_col) #add a subfigure
		self.subplot_1.spines['bottom'].set_color(self.fg_col)
		self.subplot_1.spines['left'].set_color(self.fg_col)
		self.subplot_1.patch.set_facecolor(self.bg_col)
		self.subplot_1.xaxis.set_tick_params(color=self.fg_col, labelcolor=self.fg_col)
		self.subplot_1.yaxis.set_tick_params(color=self.fg_col, labelcolor=self.fg_col)
		#add widget
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setFocusPolicy(Qt.ClickFocus )
		self.canvas.setFocus()
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.gridLayout_3.addWidget(self.canvas)
		self.gridLayout_3.addWidget(self.toolbar)
		self.canvas_1 = FigureCanvas(self.figure_1)
		self.toolbar_1 = NavigationToolbar(self.canvas_1, self)
		self.gridLayout_4.addWidget(self.canvas_1)
		self.gridLayout_4.addWidget(self.toolbar_1)
		self.canvas.mpl_connect('button_press_event', self.onclick)
		self.zp = ZoomPan()
		figZoom = self.zp.zoom_factory(self.subplot, base_scale = self.scale)
		figPan = self.zp.pan_factory(self.subplot)

	def toolbtnpressed(self,a):
		print( "pressed tool button is",a.text())

	def resizeEvent(self, event):
		self.resized.emit()
		return super(MassCalibration, self).resizeEvent(event)

	def onResize(self):
		#tight layout on resize
		self.figure.tight_layout()
		self.figure_1.tight_layout()


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
		path = os.path.dirname(sys.argv[0]) + '/config/config.ini'
		if sys.platform.startswith('darwin') or os.name == 'posix':
			res = config.read(os.path.expanduser('~')+'/.config/masscalibration/config.ini')
			if res == []:
				res == config.read(path)
				logging.warning('Configuration : config file not found in the home directory')
		else:
			res = config.read(path)

		if res!=[]:
			self.h=int(config['DEFAULT']['header'])
			self.initialDir=config['DEFAULT']['path']
			self.yCol=int(config['DEFAULT']['y'])
			self.xCol=int(config['DEFAULT']['x'])
			self.inversed=bool(int(config['DEFAULT']['inversed']))
			if bool(int(config['DEFAULT']['dark'])):
				self.fg_col = 'white'
				self.bg_col = 'black'
			else:
				self.fg_col = 'black'
				self.bg_col = 'white'
		else:
			self.showWarning('Error', 'Could not find the configuration file.\nLoading defaults')
			logging.warning('Configuration : Could not find the configuration file')
			self.h=10
			self.initialDir=os.path.dirname(sys.argv[0])
			self.yCol=2
			self.xCol=0
			self.inversed=False
			self.fg_col = 'white'
			self.bg_col = 'black'
		return config

	def ReloadConfig(self):
		self.config = self.ReadConfig()
		self.gridLayout_3.removeWidget(self.canvas)
		self.gridLayout_4.removeWidget(self.canvas_1)
		self.gridLayout_3.removeWidget(self.toolbar)
		self.gridLayout_4.removeWidget(self.toolbar_1)
		self.setTheme()
		self.Plot()
		self.lbStatus.setText("Configuration reloaded")
		logging.info("Configuration : configuration reloaded")
		self.figure.tight_layout()

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
		self.listMenu= QtWidgets.QMenu()
		menu_item_1 = self.listMenu.addAction("Plot Spectrum")
		menu_item_2 = self.listMenu.addAction("Move Up")
		menu_item_3 = self.listMenu.addAction("Move Down")
		menu_item = self.listMenu.addAction("Remove Item")
		menu_item.triggered.connect(self.menuRemoveClicked)
		menu_item_1.triggered.connect(self.menuPlotClicked)
		menu_item_2.triggered.connect(self.menuUpClicked)
		menu_item_3.triggered.connect(self.menuDownClicked)
		parentPosition = self.listWidget.mapToGlobal(QPoint(0, 0))
		self.listMenu.move(parentPosition )
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
		self.subplot_1.clear()
		self.canvas_1.draw() #draw everything to the screen
		self.files=[]
		self.decay=[]
		self.listWidget.clear()
		self.btnPlot.setEnabled(False)

	def menuPlotClicked(self):
		x, y, d = readTrc(self.files[self.listWidget.currentRow()])
		y = -y
		baseline= peakutils.baseline(abs(y))
		y = 1000*(y - baseline)
		x = x*1000
		self.subplot_1.clear()
		self.subplot_1.plot(x, y)
		self.subplot_1.set_xlabel('time of flight, ms', color=self.fg_col, fontsize = self.fontSize) #uncalibrated data
		self.subplot_1.set_ylabel('Intensity, mV', color=self.fg_col, fontsize = self.fontSize)
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
			y=-y
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
		self.subplot_1.clear()
		self.subplot_1.scatter(self.decay[:,0], self.decay[:,1])
		self.subplot_1.set_xlabel('nr of shots',color=self.fg_col, fontsize = self.fontSize)
		self.subplot_1.set_ylabel('Intensity, V s', color=self.fg_col, fontsize = self.fontSize)
		self.subplot_1.set_ylim(ymin=0)
		self.subplot_1.set_title('Decay curve', color=self.fg_col)
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
				logging.warning("Crop dialog : non valid input data")

	def Uncalibrate(self):
		if (self.Calibration.calibrated):
			self.Calibration.calibrated = False
			self.label_2.setText("")
			self.Plot()

	def Calibrate(self):
		self.Calibration.calibrate()
		self.CalibrateFormula()

	def CalibrateFormula(self):
		if self.Calibration.calibrated:
			self.Calibration.calibrated = False
		if not self.Calibration.coef[0]  ==-1:
			self.coef = np.asarray(['%.5g'%n for n in self.Calibration.coef])
			if not self.coef[1][0]=='-':
				self.coef[1] = "+"+self.coef[1]
			if not self.coef[2][0]=='-':
				self.coef[2] = "+"+self.coef[2]
			self.label_2.setText("f(t) =%s*t<sup>2</sup>%s*t%s" %(self.coef[0], self.coef[1], self.coef[2]))
			self.data.M = self.Calibration.calibration(self.data.X)
			error = self.Calibration.calcError()
			for i in np.arange(0, len(error)):
				self.tableWidget.item(i, 3).setText("%.4f"%error[i])
			self.Calibration.calibrated = True
			self.Plot()  #plot spectrum
		else:
			self.showWarning("Error", "No calibration found")
			logging.warning("Calibration : no calibration found")


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
					pos, intens, error = self.findPeak(self.data, float(time), Gfit=True, cursor=False)
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
				self.lbStatus.setText("Calibration profile loaded")
				logging.exception('Calibration : could not read the file')

#save calibration profile
	def saveCal(self):
		if not self.Calibration.calibrated:
			self.showWarning("Not calibrated!", "Please calibrate first")
			logging.warning("Save calibration : not calibrated")
			return
		path = self.initialDir
		name, _filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save calibration profile', path, "Calibration (*.mz);; All files (*.*)")
		if not name:
			return
		else:
			if name[-3:]!='.mz':
				name = name+'.mz'
			text = "Calibration coefficients\nhighest to lower power\n%.6g, %.6g, %.6g\n\nTime, Intensity, Mass, Formula, Error (ppm)" %(self.Calibration.coef[0], self.Calibration.coef[1], self.Calibration.coef[2])
			np.savetxt(name, np.column_stack((self.Calibration.peaks.values, self.Calibration.error)), header = text,fmt='%.4f,  %.1f, %.4f, %s, %.2f')
			self.lbStatus.setText("Calibration profile saved")
			logging.info("Calibration : calibration profile saved")

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
					self.xCol = 0
					self.yCol = 1
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
						logging.warning("New file : Bad column values")
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
					logging.warning('New file : Could not read the file')
					return
				except IndexError:
					self.showWarning('Error', 'Wrong delimiter')
					logging.warning('New file : Wrong delimiter')
					return
				except ValueError:
					self.showWarning('Error', 'Wrong nr of columns')
					logging.warning('New file : Wrong number of columns')
					return
			self.fname = fname
			self.setWindowTitle( ntpath.basename(fname)+ ' - Mass Spectrum Calibration - v2.3')
			self.data.setData(DataIn[:, self.xCol], DataIn[:, self.yCol])

		self.lastDrawn = 0
		self.Calibration.calibrated = False
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
					logging.info("Save : file saved")
		else:
			if not self.Calibration.calibrated:
				self.showWarning("Error", "No calibration hase been applied\nFirst calibrate your data")
				logging.warning("Calibration : no calibration has been applied")
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
				logging.info("Save : file saved")

	def SaveAs(self):
		if not self.Calibration.calibrated:
			self.showWarning("Error", "No calibration have been applied\nFirst calibrate your data")
			logging.warning("Calibration : no calibration has been applied")
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
			logging.info("file saved")

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
		msg.setText("Version v2.3 Beta\nMade by CAT\nLille, 2019")
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
		self.subplot.clear()
		if self.Calibration.calibrated:
			if self.inversed:	#plot the inversed data
				self.subplot.plot(self.data.M , self.data.max-self.data.Y[self.data.zero:])
				self.subplot.set_ylim([1.1*self.data.max,  self.data.max-self.data.min])
			else:
				self.subplot.plot(self.data.M , self.data.Y[self.data.zero:])
				self.subplot.set_ylim([self.data.min, 1.1 * self.data.max])

			self.subplot.set_xlim([self.data.M[0],500])#self.data.M[-1]]) #X axis limits
			self.subplot.set_ylabel('Intensity',color=self.fg_col, fontsize = self.fontSize)
			self.subplot.set_xlabel('m/z', color=self.fg_col, fontsize = self.fontSize) #calibrated data

		else:
			if self.inversed:	#plot the inversed data
				self.subplot.plot(self.data.X , self.data.max-self.data.Y)
				self.subplot.set_ylim([1.1*self.data.max,  self.data.max-self.data.min])
			else:
				self.subplot.plot(self.data.X , self.data.Y)
				self.subplot.set_ylim([self.data.min, 1.1 * self.data.max])
			self.subplot.set_xlim([self.data.X[0],self.data.X[self.data.len-1]]) #X axis limits
			self.subplot.set_ylabel('Intensity',color=self.fg_col, fontsize = self.fontSize)
			self.subplot.set_xlabel('time of flight', color=self.fg_col, fontsize = self.fontSize) #uncalibrated data
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

	def menuPeak(self, x, **kwargs):
		mass = -1
		text = '--'
		if self.Calibration.calibrated:
			x = np.interp(x, self.data.M, self.data.X)
		pos, intens, error = self.findPeak(self.data, x, **kwargs)
		if self.Calibration.calibrated:
			mass =	np.interp(pos, self.data.X, self.data.M)
			text = '%.4f' %mass
		if not error:
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
		menu_item_0 = self.listMenu.addAction("Remove")
		self.listMenu.addSeparator()
		menu_item_1 = self.listMenu.addAction("Remove All")
		menu_item_0.triggered.connect( self.menuRemoveRow)
		menu_item_1.triggered.connect( self.clearTable)
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
			logging.warning("Calibration : no calibration peaks")
			return False
		if -1 in self.Calibration.peaks['mass'].values:
			return False
		else:
			return True

	def menuRemoveRow(self):
		index = self.tableWidget.currentRow()
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
				logging.warning("Cell value : non numeric value")
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
			pos, intens, error = self.findPeak(self.data, self.Calibration.peaks['time'][i], Gfit = True, cursor = False )
			if not error:
				self.Calibration.peaks['time'].iloc[i] = pos
				self.Calibration.peaks['intensity'].iloc[i] = intens
				self.tableWidget.item(i, 0).setText("%.6f"%pos)
				self.tableWidget.item(i, 0).setBackground(self.tableWidget.item(0,3).background())
			else:
				self.tableWidget.item(i,0).setBackground(QColor(255,0,0))
			self.tableWidget.clearSelection()
		self.plotPeaks()


	def findPeak(self, data, x, **kwargs ):
		cursor = kwargs.get('cursor', True)
		gfit = kwargs.get('Gfit', False)
		self.min = data.min
		self.max = data.max
		width = 40
		Xpos = x
		ind=(np.abs(data.X-Xpos)).argmin()
		Ypos = data.Y[ind]
		dataX = data.X[ind-width: ind+width]
		dataY = data.Y[ind-width: ind+width]
		error = False
		if not cursor:
			try:
				indexes = peakutils.indexes(dataY,thres = 0.2, min_dist =30)
				Ypos = max(dataY[indexes])
				idx = np.argwhere(dataY==Ypos)[0]
				if gfit:
					Xpos = peakutils.interpolate(dataX, dataY, ind=idx)
				else:
					Xpos = dataX[idx]
				shift = 100*abs(Xpos-x)/x
				if shift>10:
					error = True
					Xpos = x
					self.lbStatus.setText("Failed to find a peak")
					logging.warning("Failed to find a peak")
			except RuntimeError:
				self.lbStatus.setText("Failed to find a peak")
				logging.exception("Failed to find a peak")
				error = True
		if not error:
			self.lbStatus.setText("Peak added at: %f" % Xpos)
		return Xpos, Ypos, error

#right click on the plot
	def onclick(self, event):
		if event.button == 3:  #right click
			self.listMenu= QtWidgets.QMenu()
			menu_item_0 = self.listMenu.addAction("Fit a gaussian")
			menu_item_1 = self.listMenu.addAction("Find the maximum")
			menu_item_2 = self.listMenu.addAction("Use the cursor data")
			logging.info("position: x=%f y=%f" %(event.xdata, event.ydata))
			menu_item_0.triggered.connect( lambda: self.menuPeak(event.xdata, Gfit = True, cursor=False))
			menu_item_1.triggered.connect( lambda: self.menuPeak(event.xdata, cursor = False))
			menu_item_2.triggered.connect( lambda: self.menuPeak(event.xdata))
			parentPosition = self.listWidget.mapToGlobal(QPoint(0, 0))
			cursor = QCursor()
			self.listMenu.move(cursor.pos() )
			self.listMenu.show()


app = None

def main():
	global app
	app = QApplication(sys.argv)

	form = MassCalibration()
	form.show()
	app.exec()


if __name__ == '__main__':
	main()
