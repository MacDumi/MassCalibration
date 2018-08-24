# MassCalibration
This software is designed to calibrate a time of flight mass spectrum and retrieve the variation of the signal intensity of a specific peak in a set of spectra. 

******************************************
Dependencies:
Pyqt4
matplotlib
numpy
pandas
peakutils
configparser
******************************************
Usage:
		$ python mc.py

To open a new file choose File->New (<C-n>)
To Save the mass calibration choose File->Save (ASCII), to save as npz choose File->Save as npz
You can load and save mass calibration profiles using Edit->Calibration.

Zoom:
Zoom in and out with the scroll wheel of the mouse. To zoom only on the X axis hold down the Control key <C>, for the Y axis - Shift key <S>. The plot can be moved with the mouse while holding the middle button. To activate the zooming of single axis, the focus should be on the plot.

Calibration:
Add peaks to the calibration list by right-clicking on the peak. You can choose to use the mouse coordinates or to find the closest peak. The corresponding mass can be either provided by the user or it can be calculated based on the chemical formula (the most abundant isotope).

Crop:
To crop the spectrum use the Edit->Crop option or the shortcut <C-S-c>

Baseline removal:
To remove the baseline select Edit->Remove Baseline or the shortcut <C-S-b>. A red dashed line, corresponding to the baseline, will be displayed prior to the removal.

Configuration:
The configuration file is located at ./config/config.ini and is parsed at startup. Edit it to account for your preferences.
