from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import layouts.crop_dialog as crop_dialog
import layouts.save_dialog as save_dialog
import layouts.dialog as dialog
import numpy as np
"Crop dialog"
class CropDialog (QtWidgets.QDialog, crop_dialog.Ui_Dialog):
        def __init__(self, _min, _max):
                super(CropDialog, self).__init__()
                self.setupUi(self)
                self.lbl_min.setText("%d"%_min)
                self.lbl_max.setText("%d"%_max)

        def getData(self):
                _min = self.lineEdit_min.text()
                _max = self.lineEdit_max.text()
                return _min, _max


"""Import Dialog"""
class ImportDialog (QtWidgets.QDialog, dialog.Ui_Dialog):

        def __init__(self, xCol, yCol, nCol, delim, inv):
                super(ImportDialog, self).__init__()
                self.setupUi(self)
                self.lineEdit.setEnabled(False)
                self.comboBox.activated.connect(self.other)
                if not delim <= 3:
                        delim = 0
                self.comboBox.setCurrentIndex(delim)
                self.spinBox.setValue(nCol)
                self.spinBox_2.setValue(xCol)
                self.spinBox_3.setValue(yCol)
                self.checkBox.setChecked(inv)


        def other(self):
                temp = self.comboBox.currentIndex()
                if temp == 4 :
                        self.lineEdit.setEnabled(True)
                        self.lineEdit.setPlaceholderText("specify")
                else:
                        self.lineEdit.setEnabled(False)
                        self.lineEdit.setPlaceholderText(" ")

        def getData(self):
                delimiters = ['\t', ' ', ',', '|']
                param = [self.spinBox.value()]
                param += [self.spinBox_2.value()]
                param += [self.spinBox_3.value()]
                if self.comboBox.currentIndex() == 4 :
                        delim = self.lineEdit.text()
                else:
                        delim = delimiters[self.comboBox.currentIndex()]
                param += [delim]
                param += [self.checkBox.isChecked()]

                return param
"""Save Dialog"""
class SaveDialog (QtWidgets.QDialog, save_dialog.Ui_Dialog):

        def __init__(self):
                super(SaveDialog, self).__init__()
                self.setupUi(self)
                self.comboBox.activated.connect(self.other)

        def other(self):
                temp = self.comboBox.currentIndex()
                if temp == 4 :
                        self.lineEdit.setEnabled(True)
                        self.lineEdit.setPlaceholderText("specify")
                else:
                        self.lineEdit.setEnabled(False)
                        self.lineEdit.setPlaceholderText(" ")

        def getData(self):
                delimiters = ['\t', ' ', ',', '|']
                if self.comboBox.currentIndex() == 4 :
                        param = [self.lineEdit.text()]
                else:
                        param = [delimiters[self.comboBox.currentIndex()]]
                param += [self.checkBox.isChecked()]
                return param


