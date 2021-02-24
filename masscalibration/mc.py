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
import layouts.main as main
import logging
import logging.config
import peakutils
import configparser
import time as tm
import math as mt
import h5py
from distutils.util import strtobool
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from imports.zoom import *
from imports.molmass import *
from imports.dialogs import *
from imports.data import *
from imports.calibration import *
from imports.readTrc import readTrc

VERSION = '2.5'

class MassCalibration (QMainWindow, main.Ui_MainWindow):

#initialize everything
    def __init__(self):
            super(MassCalibration, self).__init__()
            self.setupUi(self)

            #Logging
            log_level = logging.INFO
            date = datetime.now().date()
            self.config_dir = os.path.join(QStandardPaths.locate(
                    QStandardPaths.ConfigLocation, '',
                    QStandardPaths.LocateDirectory), 'masscalibration')
            log_dir = os.path.join(self.config_dir, 'logs')
            if not os.path.isdir(self.config_dir):
                os.mkdir(self.config_dir)
            if not os.path.isdir(log_dir):
                os.mkdir(log_dir)
            logging.basicConfig(filename=f'{log_dir}/{date}.log',
                   format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                   level=log_level)
            #toolbar
            self.tb = self.addToolBar("File")
            new     = QAction(QIcon("designs/new.png"), "New", self)
            save    = QAction(QIcon("designs/save.png"), "Save", self)
            save_as = QAction(QIcon("designs/saveAs.png"), "Save as", self)
            crop    = QAction(QIcon("designs/crop.png"),"Crop",self)
            loadCal = QAction(QIcon("designs/open.png"),
                                            "Load calibration", self)
            saveCal = QAction(QIcon("designs/export.png"),
                                            "Save calibration", self)
            cal = QAction(QIcon("designs/plot.png"),"Calibrate",self)
            cal_formula = QAction(QIcon("designs/plot_math.png"),
                                         "Calibrate (formula)", self)
            uncal = QAction(QIcon("designs/plot_remove.png"),
                                                 "Uncalibrate", self)
            self.tb.addAction(new)
            self.tb.addAction(save)
            self.tb.addAction(save_as)
            self.tb.addSeparator()
            self.tb.addAction(crop)
            self.tb.addSeparator()
            self.tb.addAction(loadCal)
            self.tb.addAction(saveCal)
            self.tb.addAction(cal)
            self.tb.addAction(cal_formula)
            self.tb.addAction(uncal)
            self.tb.addSeparator()
            new.triggered.connect(self.New)
            save.triggered.connect(self.save)
            save_as.triggered.connect(self.save_as)
            crop.triggered.connect(self.Crop)
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
            self.actionSave.triggered.connect(self.save)
            self.actionSaveAs.triggered.connect(self.save_as)
            self.actionUncalibrate.triggered.connect(self.Uncalibrate)
            self.actionCrop.triggered.connect(self.Crop)
            self.actionCalibrate_formula.triggered.connect(
                                                 self.CalibrateFormula)
            self.actionQuit.triggered.connect(self.close)
            self.actionCalibrate.triggered.connect(self.Calibrate)
            self.actionReloadConfig.triggered.connect(self.ReloadConfig)
            self.actionShow_toolbar.triggered.connect(
                                     self.tb.toggleViewAction().trigger)

            self.btnAdd.clicked.connect(self.addFiles)
            self.btnClear.clicked.connect(self.listClear)
            self.btnPlot.clicked.connect(self.plotDecay)
            self.pushButton_2.clicked.connect(self.menuUpClicked)
            self.pushButton.clicked.connect(self.menuDownClicked)
            self.pushButton_3.clicked.connect(self.menuRemoveClicked)
            self.btnPlot.setEnabled(False)
            self.btnPlot.setDisabled(True)


            self.scale = 1.5
            self.ReadConfig()
            self.setTheme()
            self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableWidget.customContextMenuRequested.connect(
                                            self.tableItemRightClicked)
            self.listWidget.customContextMenuRequested.connect(
                                             self.listItemRightClicked)
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
            matplotlib.rcParams.update({'font.size': self.fontSize})


    def setTheme(self):
        #calibration
        self.figure = plt.figure(edgecolor=self.fg_col,
                                                    facecolor=self.bg_col)
        self.figure.set_tight_layout(True)
        self.subplot = self.figure.add_subplot(111,
                                                    facecolor=self.bg_col)
        self.subplot.spines['bottom'].set_color(self.fg_col)
        self.subplot.spines['left'].set_color(self.fg_col)
        self.subplot.patch.set_facecolor(self.bg_col)
        self.subplot.xaxis.set_tick_params(color=self.fg_col,
                                                    labelcolor=self.fg_col)
        self.subplot.yaxis.set_tick_params(color=self.fg_col,
                                                    labelcolor=self.fg_col)
        #decay
        self.figure_1 = plt.figure(edgecolor=self.fg_col,
                                                    facecolor=self.bg_col)
        self.figure_1.set_tight_layout(True)
        self.subplot_1 = self.figure_1.add_subplot(111,
                                                    facecolor=self.bg_col)
        self.subplot_1.spines['bottom'].set_color(self.fg_col)
        self.subplot_1.spines['left'].set_color(self.fg_col)
        self.subplot_1.patch.set_facecolor(self.bg_col)
        self.subplot_1.xaxis.set_tick_params(color=self.fg_col,
                                                    labelcolor=self.fg_col)
        self.subplot_1.yaxis.set_tick_params(color=self.fg_col,
                                                    labelcolor=self.fg_col)
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
        figZoom = self.zp.zoom_factory(self.subplot, base_scale=self.scale)
        figPan = self.zp.pan_factory(self.subplot)

    def ReadConfig(self):
        self.settings = QSettings("masscalibration/settings")
        self.restoreGeometry(self.settings.value('MainWindow/geometry',
                                                    self.saveGeometry()))
        self.initialDir = self.settings.value('Data/path', './')
        self.yCol  = int(self.settings.value('Data/yCol', 2))
        self.xCol  = int(self.settings.value('Data/xCol', 0))
        self.nCol  = int(self.settings.value('Data/nCol', 3))
        self.delim = int(self.settings.value('Data/delimiter', 0))
        self.inversed = strtobool(
                    self.settings.value('Data/inversed', 'false'))
        config = configparser.ConfigParser()
        path = os.path.join(self.config_dir, 'config.ini')

        if not os.path.isfile(path):
            config.set('DEFAULT', 'header', '20')
            config.set('DEFAULT', 'dark', '0')
            config.set('DEFAULT', 'fontSize', '14')
            with open(path, 'w') as f:
                config.write(f)
        else:
            res = config.read(path)

        try:
            self.h=int(config['DEFAULT']['header'])
            self.fontSize = int(config['DEFAULT']['fontSize'])
            if bool(int(config['DEFAULT']['dark'])):
                self.fg_col = 'white'
                self.bg_col = 'black'
            else:
                self.fg_col = 'black'
                self.bg_col = 'white'
        except Exception as e:
            self.showWarning('Error',
                    f'Error while reading the config file\n{e}')
            logging.warning(f'Config file corrupted {e}')
            self.h = 20
            self.fontSize = 14
            self.fg_col = 'white'
            self.bg_col = 'black'

    def ReloadConfig(self):
        self.ReadConfig()
        self.gridLayout_3.removeWidget(self.canvas)
        self.gridLayout_4.removeWidget(self.canvas_1)
        self.gridLayout_3.removeWidget(self.toolbar)
        self.gridLayout_4.removeWidget(self.toolbar_1)
        self.setTheme()
        self.Plot()
        self.lbStatus.setText("Configuration reloaded")
        logging.info("Configuration : configuration reloaded")

    def ImportDiag(self):
        dialog = ImportDialog(self.xCol, self.yCol,
                                self.nCol, self.delim, self.inversed)
        result = dialog.exec_()
        param = 0
        param = dialog.getData()
        if result == QDialog.Accepted:
            logging.debug(f"Columns: {param[0]}\nXcl: {param[1]}"+
                    "\nYcl: {param[2]}\nsep: {param[3]}\nInv?: {param[4]}")
            return param
        return None

    def SaveDiag(self):
        dialog = SaveDialog()
        result = dialog.exec_()
        param = 0
        param = dialog.getData()
        if result == QDialog.Accepted:
            logging.debug(f"Delimiter: {param[0]}\nTwo columns: {param[1]}")
            return param
        return None

    def addFiles(self):
        files, _filter = QFileDialog.getOpenFileNames(self,
                                        'Load files', self.initialDir,
                            "Binnary files (*.trc);; All files (*.*)")
        if not files:
            return
        self.initialDir = ntpath.dirname(files[0])
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
        self.listMenu.move(parentPosition)
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
        baseline = peakutils.baseline(y)
        y = 1000 * (y - baseline)
        x = x * 1000
        self.subplot_1.clear()
        self.subplot_1.plot(x, y)
        self.subplot_1.set_xlabel('time of flight, ms', color=self.fg_col,
                                                 fontsize = self.fontSize)
        self.subplot_1.set_ylabel('Intensity, mV', color=self.fg_col,
                                                 fontsize = self.fontSize)
        self.subplot_1.set_xlim([x[0], x[-1]]) #X axis limits
        self.subplot_1.set_ylim([min(y), 1.1*max(y)])
        self.subplot_1.set_title(self.listWidget.currentItem().text())
        self.canvas_1.draw() #draw everything to the screen
        self.btnPlot.setEnabled(True)

    def plotDecay(self):
        center = np.mean(self.subplot_1.get_xlim())
        width = self.subplot_1.get_xlim()[1]-self.subplot_1.get_xlim()[0]
        logging.debug("center: %.4f\nwidth: %.4f" %(center, width))
        i=1
        nFiles = len(self.files)
        self.progressBar.setValue(0)
        out=[[0,0]]
        for i, item in enumerate(self.files):
            x, y, d = readTrc(item)
            y = -y
            baseline = peakutils.baseline(y)
            y = 1000 * (y - baseline)
            x = x * 1000
            zero  = np.argwhere(x > 0)[0]
            start = np.where(x > (center - width / 2.0))[0]
            stop  = np.where(x > (center + width / 2.0))[0]
            temp  = y[start[0]: stop[0]]
            #Integrate
            tp    = np.trapz(temp, x= x[start[0]: stop[0]])
            des   = int(ntpath.basename(item)[-7: -4])
            out   = np.append(out, [[i, tp]], axis=0)
            logging.info("file %s processed" % item)
            self.progressBar.setValue(int((i + 1) * 100 / nFiles))
        self.decay = np.delete(out, 0, axis=0)
        np.savetxt(self.initialDir+'/out.dat',
                                        self.decay, delimiter=' ')
        logging.info("output saved")
        self.subplot_1.clear()
        self.subplot_1.scatter(self.decay[:,0], self.decay[:,1])
        self.subplot_1.set_xlabel('nr of shots',
                        color=self.fg_col, fontsize = self.fontSize)
        self.subplot_1.set_ylabel('Intensity, V s',
                        color=self.fg_col, fontsize = self.fontSize)
        self.subplot_1.set_ylim(ymin=0)
        self.subplot_1.set_title('Decay curve', color=self.fg_col)
        self.progressBar.setValue(0)
        self.figure_1.savefig(self.initialDir+'/decay_fig.png')
        logging.info('figure saved')
        self.canvas_1.draw() #draw everything to the screen

    def Crop(self):
        #Crop spectrum
        if self.Calibration.calibrated:
            _min = self.data.M[0]
            _max = self.data.M[-1]
        else:
            _min = self.data.X[0]
            _max = self.data.X[-1]
        dialog = CropDialog(_min, _max)
        result = dialog.exec_()
        params = dialog.getData()
        if result == QDialog.Accepted:
            try:
                _min = int(params[0])
                _max = int(params[1])
                logging.debug(f'Cropped: {_min}, {_max}')
                self.data.crop(_min, _max, self.Calibration.calibrated)
                self.Plot()
            except ValueError:
                self.showWarning("Non valid data",
                            "Only numbers are allowed")
                logging.warning("Crop dialog : non valid input data")

    def Uncalibrate(self):
        if (self.Calibration.calibrated):
            self.Calibration.calibrated = False
            self.label_2.setText("")
            self.Plot()

    def Calibrate(self):
        #Calibrate
        self.Calibration.calibrate()
        self.CalibrateFormula()

    def CalibrateFormula(self):
        if self.Calibration.calibrated:
            self.Calibration.calibrated = False
        if not self.Calibration.coef[0]  ==-1:
            self.coef = np.asarray(
                        ['%.5g'%n for n in self.Calibration.coef])
            if not self.coef[1][0]=='-':
                self.coef[1] = "+"+self.coef[1]
            if not self.coef[2][0]=='-':
                self.coef[2] = "+"+self.coef[2]
            self.label_2.setText("f(t) =%s*t<sup>2</sup>%s*t%s" %(
                        self.coef[0], self.coef[1], self.coef[2]))
            self.data.M = self.Calibration.calibration(self.data.X)
            error = self.Calibration.calcError()
            for i in np.arange(0, len(error)):
                self.tableWidget.item(i, 3).setText("%.4f"%error[i])
            self.Calibration.calibrated = True
            self.Plot()  #plot spectrum
        else:
            self.showWarning("Error", "No calibration found")
            logging.warning("Calibration : no calibration found")

    def loadCal(self):
        #load calibration file
        fname, _filter = QFileDialog.getOpenFileName(self,
                'Load calibration profile', self.initialDir,
                "Calibration (*.mz);; All files (*.*)")
        if not fname:
            return
        else:
            self.clearTable()
            try:
                with open(fname) as f:
                    for i, line in enumerate(f):
                        if i ==2:
                            par = line
                if par[0]=='#':
                    par = par[1:]
                calibr = np.fromstring(par, dtype=float, sep=',')
                if self.Calibration.calibrated:
                    self.Uncalibrate()
                self.Calibration.clear()
                self.clearTable()
                self.Calibration.setCalibration(calibr)
                self.coef = np.asarray(['%.5g'%n for n in calibr])
                if not self.coef[1][0]=='-':
                    self.coef[1] = "+"+self.coef[1]
                if not self.coef[2][0]=='-':
                    self.coef[2] = "+"+self.coef[2]
                self.label_2.setText("f(t) =%s*t<sup>2</sup>%s*t%s" %(
                            self.coef[0], self.coef[1], self.coef[2]))

                temp = np.loadtxt(fname, delimiter=',', dtype = np.str)
                for i, time in enumerate(temp[:,0]):
                        pos, intens, error = self.findPeak(self.data,
                                    float(time), Gfit=True, cursor=False)
                        self.Calibration.addPeak([pos, intens,
                                            float(temp[i,2]), temp[i,3]])
                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)
                        self.tableWidget.setItem(rowPosition, 0,
                                            QTableWidgetItem("%.6f" % pos))
                        self.tableWidget.setItem(rowPosition, 1,
                                                QTableWidgetItem(temp[i,2]))
                        self.tableWidget.setItem(rowPosition, 2,
                                                QTableWidgetItem(temp[i,3]))
                        self.tableWidget.setItem(rowPosition, 3,
                                                     QTableWidgetItem("--"))
                self.relocatePeaks()
                self.plotPeaks()
            except IOError:
                self.showWarning('Error', 'Could not read the file')
                self.lbStatus.setText("Calibration profile loaded")
                logging.exception('Calibration : could not read the file')

    def saveCal(self):
    #save calibration profile
        if not self.Calibration.calibrated:
            self.showWarning("Not calibrated!", "Please calibrate first")
            logging.warning("Save calibration : not calibrated")
            return
        name, _filter = QFileDialog.getSaveFileName(self,
                'Save calibration profile', self.initialDir,
                            "Calibration (*.mz);; All files (*.*)")
        if not name:
            return
        else:
            if name[-3:]!='.mz':
                name = name+'.mz'
            coefs = self.Calibration.coef
            text = "Calibration coefficients\nhighest to lowest power\n"
            text += f'{coefs[0]:e}, {coefs[1]:e}, {coefs[2]:e}\n\n'
            text += "Time, Intensity, Mass, Formula, Error (ppm)"
            np.savetxt(name, np.column_stack((self.Calibration.peaks.values,
                                    self.Calibration.error)), header = text,
                                          fmt='%.4f,  %.1f, %.4f, %s, %.2f')
            self.lbStatus.setText("Calibration profile saved")
            logging.info("Calibration : calibration profile saved")

    def New(self):
        # open file dialog
        filters = {"Text files (*.txt *.dat)": self.read_txt,
                   "NPZ files (*.npz *.mc)"  : self.read_npz,
                   "Binnary files (*.trc)"   : self.read_trc,
                   "HDF5 files (*.h5)"       : self.read_hdf5,
                   "All files (*.*)"         : self.read_txt}
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file',
                            self.initialDir, ";;".join(filters.keys()))
        if not fname:
            return

        #update the initial directory for the Open/Save dialog
        self.initialDir = os.path.dirname(fname)

        if filters[_filter](fname):
            #If the file was loaded
            self.fname = fname
            self.setWindowTitle(os.path.basename(fname) +
                                 f' - Mass Spectrum Calibration - v{VERSION}')
            self.lastDrawn = 0
            self.Calibration.calibrated = False
            if len(self.Calibration.peaks['mass']):
                    self.relocatePeaks()
            #draw everything
            self.Plot()  #plot time-of-flight spectrum

    def read_trc(self, path):
        #Read the trc file
        logging.info("trc file")
        try:
            x, y, d = readTrc(path)
            self.data.setData(x, y)
            return 1
        except IOError:
            self.showWarning('Error', 'Could not read the file')
            return 0

    def read_npz(self, path):
        #Read the npz file
        logging.info("npz file")
        try:
            dt = np.load(fname)
            DataIn = dt['a']
            return 1
        except IOError:
            self.showWarning('Error', 'Could not read the file')
            return 0

    def read_hdf5(self, path):
        #Read an HDF5 file
        try:
            with h5py.File(path, 'r') as f:
                if 'tof_data' in f.keys():
                    x = f['tof_data']['time'][()]
                    y = f['tof_data']['average'][()]
                    self.data.setData(x, y)
                else:
                    logging.info(f'No tof_data dataset')
                    self.showWarning('Error', f'Unknown file structure')
            return 1
        except Exception as e:
            logging.error(f'Could not read the file\n{e}')
            self.showWarning('Error', f'Could not read the file\n{e}')
            return 0

    def read_txt(self, path):
        #Read an ASCII file
        logging.info("text file")
        params = self.ImportDiag() #display dialog for import options
        if params:
            if (params[1] + 1 > params[0] or
                params[2] + 1 > params[0]) :
                self.showWarning("Error", "bad column values")
                logging.warning("New file : Bad column values")
            else:
                self.xCol= params[1]
                self.yCol= params[2]
                self.inversed = params[4]
                try:
                    #read a text file
                    data = np.loadtxt(path,
                              skiprows=self.h,
                              usecols=range(params[0]),
                              delimiter=params[3])
                    self.data.setData(data[:,self.xCol], data[:,self.yCol])
                    return 1
                except IOError as e:
                    self.showWarning('Error',
                        f'Could not read the file\n{e}')
                    logging.warning(
                    'New file : Could not read the file')
                    return 0
                except IndexError as e:
                    self.showWarning('Error',
                            f'Wrong delimiter\n{e}')
                    logging.warning(
                        'New file : Wrong delimiter')
                    return 0
                except ValueError as e:
                    self.showWarning('Error',
                        f'Wrong nr of columns\n{e}')
                    logging.warning(
                    'New file : Wrong number of columns')
                    return 0

    def save(self):
        ext = os.path.splitext(self.fname)[1]
        if ext == '.npz':
            save_func = self.save_npz
        elif ext == '.h5':
            save_func = self.save_h5
        else:
            save_func = lambda name: self.save_txt(name, update=True)

        try:
            if save_func(self.fname):
                logging.info(f'File {self.fname} saved')
                self.lbStatus.setText("File saved")
        except Exception as e:
            self.showWarning('Error', f'Could not save the file\n{e}')
            logging.warning(f'Could not save the file : {e}')

    def save_as(self):
        #Save the calibrated spectrum
        filters = {"Text files (*.txt *.dat)": self.save_txt,
                   "NPZ files (*.npz *.mc)"  : self.save_npz,
                   "All files (*.*)"         : self.save_txt}
        name, _filter = QFileDialog.getSaveFileName(self, 'Save file',
                                        self.fname, ";;".join(filters))
        if not name:
            return

        if self.tabWidget.currentIndex() == 1:
            if self.decay!=[]:
                np.savetxt(name, self.decay, header="Signal decay",
                                                        delimiter='\t')
        else:
            if not self.Calibration.calibrated:
                self.showWarning("Error", "Calibrate first")
                logging.warning("Calibration : no calibration")
            else:
                try:
                    if filters[_filter](name):
                        logging.info(f'File {name} saved')
                        self.lbStatus.setText("File saved")
                except Exception as e:
                    self.showWarning('Error',
                                f'Could not save the file\n{e}')
                    logging.warning(f'Could not save the file : {e}')

    def save_txt(self, path, update=False):
        #Save a txt file
        if not update:
            params = self.SaveDiag()
            if params is None:
                return 0
        else:
            params = ('\t', False)

        x    = self.data.X[self.data.limits[0]:self.data.limits[1]]
        mass = self.data.M[self.data.limits[0]:self.data.limits[1]]

        if self.inversed:
            y = self.data.max-self.data.Y[
                    self.data.limits[0]:self.data.limits[1]]
        else:
            y = self.data.Y[self.data.limits[0]:self.data.limits[1]]

        if params[1]:
            np.savetxt(path, np.transpose([mass, y]), delimiter=params[0])
        else:
            header = "Calibrated Mass Spectrum\nCalibration coefficients\n"
            header += f'{self.coef[0]}, {self.coef[1]}, {self.coef[2]}\n'
            header += "time\tmass\tsignal"
            np.savetxt(path, np.transpose([x, mass, y]), header=header,
                                                      delimiter=params[0])
        return 1

    def save_npz(self, path):
        #Save a file as npz
        x    = self.data.X[self.data.limits[0]:self.data.limits[1]]
        mass = self.data.M[self.data.limits[0]:self.data.limits[1]]
        if self.inversed:
            y = self.data.max-self.data.Y[
                        self.data.limits[0]:self.data.limits[1]]
        else:
            y = self.data.Y[self.data.limits[0]:self.data.limits[1]]

        if self.save2col:
            np.savez_compressed(name, a=np.transpose([mass, y]))
        else:
            np.savez_compressed(name, a=np.transpose([x, mass, y]))
        return 1

    def save_h5(self, name):
        with h5py.File(name, 'r+') as f:
            f['tof_data']['mass'][:] = self.data.M
            f.flush()
        return 1

    def showWarning(self, title, message):
        #warning pop-up message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def about(self):
        #information pop-up message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Version v{VERSION} Beta\nMade by MacDumi\nLille, 2020")
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

    def Plot(self):
        #Plot the data
        try:
            self.subplot.clear()
            limits = self.data.limits
            if self.inversed:
                y = self.data.max = self.data.Y[limits[0]:limits[1]]
            else:
                y = self.data.Y[limits[0]:limits[1]]
            if self.Calibration.calibrated:
                self.subplot.plot(self.data.M[limits[0]:limits[1]], y)

                self.subplot.set_xlim([self.data.M[limits[0]], 500])
                self.subplot.set_ylabel('Intensity', color=self.fg_col,
                                                    fontsize = self.fontSize)
                self.subplot.set_xlabel('m/z', color=self.fg_col,
                                                    fontsize = self.fontSize)
                self.subplot.format_coord = lambda x, y: f'm/z={x:.3f}'
            else:
                self.subplot.plot(self.data.X[limits[0]:limits[1]], y)
                self.subplot.set_xlim([self.data.X[limits[0]],
                                                      self.data.X[limits[1]]])
                self.subplot.set_ylabel('Intensity', color=self.fg_col,
                                                     fontsize = self.fontSize)
                self.subplot.set_xlabel('time of flight', color=self.fg_col,
                                                     fontsize = self.fontSize)
                self.subplot.format_coord = lambda x, y: f'ToF={x:.2f}'
            self.cursor = Cursor(self.subplot, horizOn=False, useblit=True,
                                     color='red', linestyle='--', linewidth=1)
            self.scatter = 0
            self.plotPeaks()
            self.canvas.draw() #draw everything to the screen
        except AttributeError:
            logging.warning('no data to be plotted')

    def plotPeaks(self):
        self.removeScatter()
        if (self.Calibration.peaks['mass'].shape):
            if (self.Calibration.calibrated):
                self.scatter = self.subplot.scatter(
                        self.Calibration.peaks['mass'],
                        self.Calibration.peaks['intensity'],
                        s =70, facecolors='r', marker='v')
            else:
                self.scatter = self.subplot.scatter(
                        self.Calibration.peaks['time'],
                        self.Calibration.peaks['intensity'],
                        s =70, facecolors='r', marker='v')
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
            mass =  np.interp(pos, self.data.X, self.data.M)
            text = '%.4f' %mass
        if not error:
            self.Calibration.addPeak([pos, intens, mass, '--'])
            rowPosition = self.tableWidget.rowCount()
            self.plotPeaks()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0,
                                  QTableWidgetItem(f"{pos:.6f}"))
            self.tableWidget.setItem(rowPosition, 1,
                                          QTableWidgetItem(text))
            self.tableWidget.setItem(rowPosition, 2,
                                          QTableWidgetItem("--"))
            self.tableWidget.setItem(rowPosition, 3,
                                          QTableWidgetItem("--"))

    def tableItemRightClicked(self, QPos):
        self.listMenu= QMenu()
        menu_item_0 = self.listMenu.addAction("Remove")
        self.listMenu.addSeparator()
        menu_item_1 = self.listMenu.addAction("Remove All")
        menu_item_0.triggered.connect(self.menuRemoveRow)
        menu_item_1.triggered.connect(self.clearTable)
        parentPosition = self.tableWidget.mapToGlobal(QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def clearTable(self):
            while self.tableWidget.rowCount()!=0:
                self.tableWidget.setCurrentCell(0, 0)
                self.menuRemoveRow()

    def checkMasses(self):
        if len(self.Calibration.peaks['mass'].values)==0:
            self.showWarning("No calibration data", "Please add calibration peaks")
            logging.warning("Calibration : no calibration peaks")
            return False
        if -1 in self.Calibration.peaks['mass'].values:
            return False
        return True

    def menuRemoveRow(self):
        index = self.tableWidget.currentRow()
        self.tableWidget.removeRow(index)
        self.Calibration.removePeak(index)
        if (self.scatter):
            self.scatter.remove()
        if (self.Calibration.calibrated):
            self.scatter = self.subplot.scatter(
                         self.Calibration.peaks['mass'],
                    self.Calibration.peaks['intensity'],
                      s =70, facecolors='r', marker='v')
        else:
            self.scatter = self.subplot.scatter(
                         self.Calibration.peaks['time'],
                    self.Calibration.peaks['intensity'],
                      s =70, facecolors='r', marker='v')
        self.canvas.draw()

    def cellchanged(self):
        col = self.tableWidget.currentColumn()
        if col ==1:
            try:
                mass= float(self.tableWidget.currentItem().text())
                self.tableWidget.currentItem().setBackground(
                               self.tableWidget.item(0,0).background())
                self.Calibration.setMass(self.tableWidget.currentRow(),
                                                          [mass, '--'])
            except ValueError:
                logging.warning("Cell value : non numeric value")
                self.tableWidget.currentItem().setBackground(
                                                       QColor(255,0,0))
            self.tableWidget.clearSelection()
        elif col ==2:
            try:
                mass= Formula(
                        self.tableWidget.currentItem().text()).isotope.mass
                self.tableWidget.currentItem().setBackground(
                                   self.tableWidget.item(0,0).background())
                self.tableWidget.item(
                     self.tableWidget.currentRow(), 1).setText("%.4f"%mass)
                self.Calibration.setMass(self.tableWidget.currentRow(),
                             [mass, self.tableWidget.currentItem().text()])
            except FormulaError:
                self.tableWidget.currentItem().setBackground(
                                                           QColor(255,0,0))
            self.tableWidget.clearSelection()

    def relocatePeaks (self):
        logging.debug(f"peak calibration: {self.Calibration.peaks['time']}")
        for i in np.arange(0, len(self.Calibration.peaks['time'])):
                pos, intens, error = self.findPeak(self.data,
                            self.Calibration.peaks['time'][i],
                                 Gfit = True, cursor = False )
                if not error:
                        self.Calibration.peaks['time'].iloc[i] = pos
                        self.Calibration.peaks['intensity'].iloc[i]= intens
                        self.tableWidget.item(i, 0).setText("%.6f"%pos)
                        self.tableWidget.item(i, 0).setBackground(
                                    self.tableWidget.item(0,3).background())
                else:
                        self.tableWidget.item(i,0).setBackground(
                                                            QColor(255,0,0))
                self.tableWidget.clearSelection()
        self.plotPeaks()

    def findPeak(self, data, x, cursor=True, Gfit=False, **kwargs):
        self.min = data.min
        self.max = data.max
        width = 40
        Xpos  = x
        ind   = (np.abs(data.X-Xpos)).argmin()
        Ypos  = data.Y[ind]
        dataX = data.X[ind-width: ind+width]
        dataY = data.Y[ind-width: ind+width]
        error = False
        if not cursor:
            try:
                indexes = peakutils.indexes(dataY,
                                                thres = 0.2, min_dist =30)
                if len(indexes)<1:
                    indexes = peakutils.indexes(dataY,
                                                thres = 0.1, min_dist = 20)
                Ypos = max(dataY[indexes])
                idx = np.argwhere(dataY==Ypos)[0]
                if Gfit:
                    Xpos = peakutils.interpolate(dataX, dataY, ind=idx)[0]
                else:
                    Xpos = dataX[idx][0]
                shift = 100*abs(Xpos-x)/x
                if shift>10:
                    error = True
                    Xpos = x
                    self.lbStatus.setText("Failed to find a peak")
                    logging.warning("Failed to find a peak")
            except (RuntimeError, ValueError):
                self.lbStatus.setText("Failed to find a peak")
                logging.exception("Failed to find a peak")
                error = True
        if not error:
            self.lbStatus.setText("Peak added at: %f" % Xpos)
        return Xpos, Ypos, error

    def onclick(self, event):
        #right click on the plot
        if event.button == 3:  #right click
            self.listMenu= QMenu()
            menu_item_0 = self.listMenu.addAction("Fit a gaussian")
            menu_item_1 = self.listMenu.addAction("Find the maximum")
            menu_item_2 = self.listMenu.addAction("Use the cursor data")
            logging.info("position: x=%f y=%f" %(event.xdata, event.ydata))
            menu_item_0.triggered.connect( lambda: self.menuPeak(
                                    event.xdata, Gfit = True, cursor=False))
            menu_item_1.triggered.connect( lambda: self.menuPeak(
                                               event.xdata, cursor = False))
            menu_item_2.triggered.connect( lambda: self.menuPeak(
                                                               event.xdata))
            parentPosition = self.listWidget.mapToGlobal(QPoint(0, 0))
            cursor = QCursor()
            self.listMenu.move(cursor.pos())
            self.listMenu.show()

    def closeEvent(self, event):
        self.settings.setValue('MainWindow/geometry', self.saveGeometry())
        self.settings.setValue('Data/path', self.initialDir)
        self.settings.setValue('Data/yCol', self.yCol)
        self.settings.setValue('Data/xCol', self.xCol)
        self.settings.setValue('Data/nCol', self.nCol)
        self.settings.setValue('Data/delimiter', self.delim)
        self.settings.setValue('Data/inversed', self.inversed)
        event.accept()


if __name__ == '__main__':
    app = QApplication([sys.argv])
    application = MassCalibration()
    application.show()
    app.exec()

