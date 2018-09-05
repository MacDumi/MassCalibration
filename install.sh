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

		install -d ./config $DATADIR/config
		install -m644 ./config/* $DATADIR/config/

		install -d ./imports $DATADIR/imports
		install -m644 ./imports/* $DATADIR/imports/

		cd $STARTDIR/install
		install -m755 * $DESKDIR/

		install -d $BINDIR
		ln -s $DATADIR/mc.py $BINDIR/masscalibration

		echo "done."

		exit 0

