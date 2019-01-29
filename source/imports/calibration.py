import numpy as np
import pandas as pd
import logging


"""Calibration data"""
class Calibration:

	def __init__(self):
		super(Calibration, self).__init__()
		self.peaks = pd.DataFrame(columns=['time', 'intensity', 'mass', 'formula'])
		self.calibrated = False #True when the data is calibrated
		self.coef = [-1, -1, -1]

	def calibrate(self):
		print(self.peaks)
		self.coef = np.polyfit(self.peaks['time'].astype('float'), self.peaks['mass'].astype('float'), 2)
		print(self.coef)
		self.calibration = np.poly1d(self.coef)
		self.calibrated = True
		return self.coef

	def addPeak(self, params):
		self.peaks.loc[self.peaks.shape[0]] = params
		logging.info('Calibration : peak at %f added' %params[0])

	def removePeak(self, index):
		self.peaks.drop(index, inplace=True)
		self.peaks = self.peaks.reset_index(drop=True)

	def clear(self):
		self.peaks = pd.DataFrame(columns=['time', 'intensity', 'mass', 'formula'])
		self.calibrated = False
		self.coef = [-1,-1, -1]

	def setCalibration(self, coef):
		try:
			self.calibration = np.poly1d(coef)
			self.coef = coef
			logging.info("Calibration : Parameters loaded")
		except Exception:
			logging.exception("Calibration : Bad values")

	def setMass(self, index, params):
		self.peaks.iloc[index, 2]=params[0]
		self.peaks.iloc[index, 3]=params[1]


	def calcError(self):
		self.error = []
		MM = self.calibration(self.peaks['time'])
		self.error = 1e6*(self.peaks['mass'] - MM)/MM
		print('Error:\n',self.error)
		return self.error

	def inMass(self, time):
		return self.calibration(time)


