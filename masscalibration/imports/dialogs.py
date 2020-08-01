from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import crop_dialog
import save_dialog
import dialog
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

        def __init__(self, config):
                super(ImportDialog, self).__init__()
                self.setupUi(self)
                self.lineEdit.setEnabled(False)
                self.comboBox.activated.connect(self.other)
                idx = int(config['DEFAULT']['delimiter'])
                if not idx<=3:
                        idx =0
                self.comboBox.setCurrentIndex(idx)
                self.spinBox.setValue(int(config['DEFAULT']['nCol']))
                self.spinBox_2.setValue(int(config['DEFAULT']['X']))
                self.spinBox_3.setValue(int(config['DEFAULT']['Y']))
                self.checkBox.setChecked(int(config['DEFAULT']['inversed']))


        def other(self):
                temp = self.comboBox.currentIndex()
                print(temp)
                if temp == 4 :
                        self.lineEdit.setEnabled(True)
                        self.lineEdit.setPlaceholderText("specify")
                else:
                        self.lineEdit.setEnabled(False)
                        self.lineEdit.setPlaceholderText(" ")

        def getData(self):
                delimiters = [' ', ' ', ',', '|']
                param = self.spinBox.value()
                param = np.append(param, self.spinBox_2.value())
                param = np.append(param, self.spinBox_3.value())
                if self.comboBox.currentIndex() == 4 :
                        delim = self.lineEdit.text()
                else:
                        delim = delimiters[self.comboBox.currentIndex()]
                param = np.append(param, delim)
                if self.checkBox.isChecked():
                        param = np.append(param, 1)
                else:
                        param = np.append(param, 0)

                return param
"""Save Dialog"""
class SaveDialog (QtWidgets.QDialog, save_dialog.Ui_Dialog):

        def __init__(self):
                super(SaveDialog, self).__init__()
                self.setupUi(self)
                self.comboBox.activated.connect(self.other)

        def other(self):
                temp = self.comboBox.currentIndex()
                print(temp)
                if temp == 4 :
                        self.lineEdit.setEnabled(True)
                        self.lineEdit.setPlaceholderText("specify")
                else:
                        self.lineEdit.setEnabled(False)
                        self.lineEdit.setPlaceholderText(" ")

        def getData(self):
                delimiters = [' ', ' ', ',', '|']
                if self.comboBox.currentIndex() == 4 :
                        param = self.lineEdit.text()
                else:
                        param = delimiters[self.comboBox.currentIndex()]
                if self.checkBox.isChecked():
                        param = np.append(param, 1)
                else:
                        param = np.append(param, 0)
                return param


