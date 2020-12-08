#!/bin/bash


        STARTDIR=$PWD
        BINDIR="/usr/bin"
        DATADIR="/usr/lib/masscalibration"
        DESKDIR="/usr/share/applications"


        echo "Installing Mass Calibration ... "

        cd $STARTDIR/masscalibration
        install -d $DATADIR
        install -m644 *.* $DATADIR/
        install -m755 mc.py $DATADIR/

        install -d ./imports $DATADIR/imports
        install -m644 ./imports/* $DATADIR/imports/

        install -d ./designs $DATADIR/designs
        install -m644 ./designs/* $DATADIR/designs/

        install -d ./layouts $DATADIR/layouts
        install -m644 ./layouts/* $DATADIR/layouts/

        cd $STARTDIR
        install -m755 MassCalibration.desktop $DESKDIR/

        install -d $BINDIR
        if test -f "$BINDIR/masscalibration"; then
            rm $BINDIR/masscalibration
            echo "Removing old symbolic links"
        fi
        ln -s $DATADIR/mc.py $BINDIR/masscalibration

        echo "done."

        exit 0

