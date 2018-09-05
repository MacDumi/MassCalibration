import numpy as np

""" object for initial and calculated data"""
class Data:
	def __init__(self):
		super(Data, self).__init__()
	def setData(self, _X, _Y):
		self.X = _X
		self.Y = _Y
		self.len= len(self.X)
		self.max = max(self.Y)
		self.min = min(self.Y)
		self.M = np.zeros(self.len)
		self.zero=0
		print ("Min value ", self.min)
		print ("Max value ",self.max)

	def crop(self, _min, _max, calibrated):
		if calibrated:
			if _min <= self.M[0]:
				min_idx = 0
			else:
				min_idx = np.argwhere(self.M>=_min)[0][0]
			if _max >= self.M[-1]:
				max_idx = -1
			else:
				max_idx = np.argwhere(self.M>=_max)[0][0]
		else:
			if _min <= self.X[0]:
				min_idx = 0
			else:
				min_idx = np.argwhere(self.X>=_min)[0][0]
			if _max >= self.X[-1]:
				max_idx = -1
			else:
				max_idx = np.argwhere(self.X>=_max)[0][0]
		print(min_idx, max_idx)
		self.X = self.X[min_idx:max_idx]
		self.M = self.M[min_idx:max_idx]
		self.Y = self.Y[min_idx:max_idx]
		self.max = max(self.Y)
		self.min = min(self.Y)
		self.len = len(self.X)

	def setMass(self, calibration):

		self.M = calibration.A*np.power((self.X - calibration.t0),2)
		self.zero = np.argmin(self.M)
		self.M = self.M[self.zero:]
		print("Calibration applied")
		print(self.M)


