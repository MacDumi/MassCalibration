import numpy as np
import logging

""" object for initial and calculated data"""
class Data:
    def __init__(self):
        super(Data, self).__init__()

    def setData(self, _X, _Y):
        #load new data
        self.X = _X
        self.Y = _Y
        self.len = len(self.X)
        self.max = max(self.Y)
        self.min = min(self.Y)
        self.M = np.zeros(self.len)
        self.limits  = [0, self.len - 1]
        self.baseline = np.zeros(self.len)
        if self.X[-1]<1:
            self.X *= 1e6
            logging.warning("New spectrum : X correction - 1e6")
        if (self.max-self.min)<=1:
            self.Y *= 1e6
            logging.warning("New spectrum : Y correction - 1e6")
            self.max = max(self.Y)
            self.min = min(self.Y)
        if self.X[0]<0:
            self.crop(0, self.X[-1])
        logging.info("New spectrum : Min value %f" %self.min)
        logging.info("New spectrum : Max value %f" %self.max)

    def crop(self, _min, _max, calibrated=False):
        #crop the spectrum
        if calibrated:
            try:
                self.limits[0] = np.where(self.M >= _min)[0][0]
                self.limits[1] = np.where(self.M >= _max)[0][0]
                logging.info(f"Cropped to {_min}, {_max} m/z")
            except IndexError:
                logging.warning(f"Could not crop to {_min, _max}")
        else:
            try:
                self.limits[0] = np.where(self.X >= _min)[0][0]
                self.limits[1] = np.where(self.X >= _max)[0][0]
                logging.info(f"Cropped to {_min}, {_max}")
            except IndexError:
                logging.warning(f"Could not crop to {_min, _max}")
        self.max = max(self.Y[self.limits[0]:self.limits[1]])
        self.min = min(self.Y[self.limits[0]:self.limits[1]])

    def setMass(self, calibration):
        self.M = calibration.A*np.power((self.X - calibration.t0),2)
        self.zero = np.argmin(self.M)
        self.M = self.M[self.zero:]
        logging.info("Calibration applied")

    def remove_baseline(self, baseline):
        if len(baseline) == self.len:
            self.Y = self.Y + self.baseline - baseline
            self.baseline = baseline
            logging.info('Baseline removed')
        else:
            logging.warning("Baseline removal: shape mismatch")
