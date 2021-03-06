# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1161, 776)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("designs/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("file:///home/cat/Workspace/QTDark/QTDark.stylesheet")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_3.sizePolicy().hasHeightForWidth())
        self.tab_3.setSizePolicy(sizePolicy)
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(self.tab_3)
        self.splitter.setMinimumSize(QtCore.QSize(150, 0))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setStyleSheet("file:///home/cat/Workspace/QTDark/QTDark.stylesheet")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.lbStatus = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbStatus.setText("")
        self.lbStatus.setObjectName("lbStatus")
        self.verticalLayout_2.addWidget(self.lbStatus)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout.addLayout(self.gridLayout_4, 1, 0, 7, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAdd = QtWidgets.QPushButton(self.tab_4)
        self.btnAdd.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAdd.sizePolicy().hasHeightForWidth())
        self.btnAdd.setSizePolicy(sizePolicy)
        self.btnAdd.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../designs/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon1)
        self.btnAdd.setIconSize(QtCore.QSize(30, 30))
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../designs/arrow-up.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.tab_4)
        self.pushButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../designs/arrow-down.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon3)
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_3.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../designs/remove.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon4)
        self.pushButton_3.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 3, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnPlot = QtWidgets.QPushButton(self.tab_4)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../designs/plot.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPlot.setIcon(icon5)
        self.btnPlot.setIconSize(QtCore.QSize(30, 30))
        self.btnPlot.setObjectName("btnPlot")
        self.horizontalLayout_2.addWidget(self.btnPlot)
        self.btnClear = QtWidgets.QPushButton(self.tab_4)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../designs/clear.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClear.setIcon(icon6)
        self.btnClear.setIconSize(QtCore.QSize(28, 28))
        self.btnClear.setObjectName("btnClear")
        self.horizontalLayout_2.addWidget(self.btnClear)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_4)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 3, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.tab_4)
        self.listWidget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listWidget.setLineWidth(2)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 3, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.tab_4)
        self.progressBar.setEnabled(False)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 0))
        self.progressBar.setMaximumSize(QtCore.QSize(300, 16777215))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 3, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1161, 34))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTearOffEnabled(True)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionInstructions = QtWidgets.QAction(MainWindow)
        self.actionInstructions.setObjectName("actionInstructions")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionRm_baseline = QtWidgets.QAction(MainWindow)
        self.actionRm_baseline.setObjectName("actionRm_baseline")
        self.actionReloadConfig = QtWidgets.QAction(MainWindow)
        self.actionReloadConfig.setObjectName("actionReloadConfig")
        self.actionCrop = QtWidgets.QAction(MainWindow)
        self.actionCrop.setObjectName("actionCrop")
        self.actionCalibrate = QtWidgets.QAction(MainWindow)
        self.actionCalibrate.setObjectName("actionCalibrate")
        self.actionUncalibrate = QtWidgets.QAction(MainWindow)
        self.actionUncalibrate.setAutoRepeat(True)
        self.actionUncalibrate.setObjectName("actionUncalibrate")
        self.actionLoadProfile = QtWidgets.QAction(MainWindow)
        self.actionLoadProfile.setObjectName("actionLoadProfile")
        self.actionSaveProfile = QtWidgets.QAction(MainWindow)
        self.actionSaveProfile.setObjectName("actionSaveProfile")
        self.actionCalibrate_formula = QtWidgets.QAction(MainWindow)
        self.actionCalibrate_formula.setObjectName("actionCalibrate_formula")
        self.actionShow_toolbar = QtWidgets.QAction(MainWindow)
        self.actionShow_toolbar.setCheckable(True)
        self.actionShow_toolbar.setChecked(True)
        self.actionShow_toolbar.setObjectName("actionShow_toolbar")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCrop)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionShow_toolbar)
        self.menuEdit.addAction(self.actionReloadConfig)
        self.menuHelp.addAction(self.actionInstructions)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuTools.addAction(self.actionCalibrate)
        self.menuTools.addAction(self.actionCalibrate_formula)
        self.menuTools.addAction(self.actionUncalibrate)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionLoadProfile)
        self.menuTools.addAction(self.actionSaveProfile)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mass Calibration - v2.5"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Time"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Mass"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Formula"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Error (ppm)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Mass Calibration"))
        self.btnPlot.setText(_translate("MainWindow", "Plot the decay "))
        self.btnClear.setText(_translate("MainWindow", "Clear All"))
        self.label.setText(_translate("MainWindow", "Select the peak by zooming on it"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Signal decay"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuEdit.setTitle(_translate("MainWindow", "E&dit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Calibratio&n"))
        self.actionNew.setText(_translate("MainWindow", "&Open"))
        self.actionNew.setIconText(_translate("MainWindow", "Open"))
        self.actionNew.setToolTip(_translate("MainWindow", "Open a file"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_as.setText(_translate("MainWindow", "Sa&ve as npz"))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionPreferences.setText(_translate("MainWindow", "&Preferences"))
        self.actionPreferences.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionInstructions.setText(_translate("MainWindow", "&Instructions"))
        self.actionAbout.setText(_translate("MainWindow", "&About"))
        self.actionRm_baseline.setText(_translate("MainWindow", "&Remove baseline"))
        self.actionRm_baseline.setShortcut(_translate("MainWindow", "Ctrl+Shift+B"))
        self.actionReloadConfig.setText(_translate("MainWindow", "Reload &config"))
        self.actionReloadConfig.setShortcut(_translate("MainWindow", "Ctrl+Shift+U"))
        self.actionCrop.setText(_translate("MainWindow", "Cr&op"))
        self.actionCrop.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.actionCalibrate.setText(_translate("MainWindow", "&Calibrate"))
        self.actionCalibrate.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionUncalibrate.setText(_translate("MainWindow", "&Uncalibrate"))
        self.actionUncalibrate.setShortcut(_translate("MainWindow", "Ctrl+Shift+R"))
        self.actionLoadProfile.setText(_translate("MainWindow", "&Load profile"))
        self.actionSaveProfile.setText(_translate("MainWindow", "&Save profile"))
        self.actionCalibrate_formula.setText(_translate("MainWindow", "Calibrate (&formula)"))
        self.actionShow_toolbar.setText(_translate("MainWindow", "&Show toolbar"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save As"))
        self.actionSaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
