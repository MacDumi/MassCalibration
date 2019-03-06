# MassCalibration
This software is designed to calibrate a time of flight mass spectrum and retrieve the variation of the signal intensity of a specific peak in a set of spectra. 

## Dependencies:
Pyqt5, matplotlib, numpy, pandas, peakutils, configparser

## Usage:

    $ python mc.py

To open a new file choose File->New (**C-n**)
To Save the mass calibration choose **File->Save** (ASCII), to save as *npz* choose **File->Save as npz**.
The toolbar can be either displayed or hidden (**Edit->Toolbar**).

### Configuration:

The configuration file is located at *./config/config.ini* and is parsed at startup. 
Edit it to account for your preferences (default delimiter, number of columns to import, font size and theme).
To reload the configuration file choose **Edit->Reload Config**.

### Calibration:

To calibrate a mass spectrum:

* Import a new uncalibrated mass spectrum
* Load an existing calibration file (**Calibration->Load profile**) and calibrate using the calibration formula to get a rough calibration (**Calibrate->Calibrate(formula)**).
**Note: The obtained calibration should only be used as a starting point for a more precise calibration and cannot be considered a final result.**
	* If you don't have a calibration file suitable for your mass range you can directly move to the next stage;
* Calibrate your spectrum with a peaklist. To create a peakilst:
	* Locate the peak with a known mass and add it to the list by right-clicking on it and selecting a suitable peak-detecting algorithm.
	* Add as many peaks as you can. For a good calibration, the peaklist should cover the majority of the mass rage.
	* Once you added a peak you need to specify its corresponding mass. The mass can either be added manually or calculated from the chemical formula (e.g. C14H10). In case of syntax errors, the background of the cell will become red.
	*Note: The mass of a specific isotope can be also calculated (e.g. **13C**C13H10).*
	* When the peaklist is complete you can calibrate your spectrum with it: (**C-r**) or Calibration->Calibrate. The error in ppm will be calculated for each mass peak and the calibration equation will be displayed on top of the peaklist.
	* To go back to the time-of-flight spectrum choose **Calibration->Uncalibrate** or (**C-S-r**).

You can save mass calibration profiles by choosing **Edit->Calibration**.
If a peaklist is present when a new spectrum is loaded, the software will attempt to locate the peaks on in the new spectrum thus allowing the user to immediately calibrate. In case the algorithm fails to find one or several peaks they will be marked in red. The user should remove them or manually locate them on the spectrum.

### Zoom:

Zoom in and out with the scroll wheel of the mouse. To zoom only on the X axis hold down the Control key (**C**), for the Y axis - Shift key (**S**). The plot can be moved with the mouse while holding the middle button. To activate the zooming of single axis, the focus should be on the plot.

### Crop:

To crop the spectrum use the **Edit->Crop** option or the shortcut (**C-S-c**)

### Baseline removal:

To remove the baseline select **Edit->Remove Baseline** or the shortcut (**C-S-b**). A red dashed line, corresponding to the baseline, will be displayed prior to the removal.

