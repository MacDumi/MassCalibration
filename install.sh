#!/bin/bash


		STARTDIR=$PWD
		BINDIR="/usr/bin"
		DATADIR="/usr/lib/masscalibration"
		DESKDIR="/usr/share/applications"


		echo -n "Installing Mass Calibration ... "

		cd $STARTDIR/source
		install -d $DATADIR
		install -m644 *.* $DATADIR/
		install -m755 mc.py $DATADIR/

		install -d ./config $HOME/.config/masscalibration/
		install -m644 ./config/* $HOME/.config/masscalibration

		install -d ./imports $DATADIR/imports
		install -m644 ./imports/* $DATADIR/imports/

		install -d ./logs $DATADIR/logs
		install -m644 ./logs/* $DATADIR/logs/

		cd $STARTDIR/install
		install -m755 * $DESKDIR/

		install -d $BINDIR
		ln -s $DATADIR/mc.py $BINDIR/masscalibration

		echo "done."

		exit 0

