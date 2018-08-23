# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crop_dialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(284, 145)
        Dialog.setMaximumSize(QtCore.QSize(284, 145))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 110, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lbl_max = QtGui.QLabel(Dialog)
        self.lbl_max.setGeometry(QtCore.QRect(190, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_max.setFont(font)
        self.lbl_max.setText(_fromUtf8(""))
        self.lbl_max.setObjectName(_fromUtf8("lbl_max"))
        self.lbl_min = QtGui.QLabel(Dialog)
        self.lbl_min.setGeometry(QtCore.QRect(30, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_min.setFont(font)
        self.lbl_min.setText(_fromUtf8(""))
        self.lbl_min.setObjectName(_fromUtf8("lbl_min"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 0, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_min = QtGui.QLineEdit(Dialog)
        self.lineEdit_min.setGeometry(QtCore.QRect(20, 40, 91, 32))
        self.lineEdit_min.setObjectName(_fromUtf8("lineEdit_min"))
        self.lineEdit_max = QtGui.QLineEdit(Dialog)
        self.lineEdit_max.setGeometry(QtCore.QRect(170, 40, 91, 32))
        self.lineEdit_max.setObjectName(_fromUtf8("lineEdit_max"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Crop to", None))

