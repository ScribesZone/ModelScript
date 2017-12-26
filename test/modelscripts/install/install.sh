#!/usr/bin/env bash

XXXX
exit
# ssh favreje@mandelbrot.e.ujf-grenoble.fr
INSTALL=/home/f/favreje/public
MODELSCRIBES_VENV=${INSTALL?}/bin
MODELSCRIBES_HOME=${INSTALL?}/ModelScribes

# /home/f/favreje/public/ModelScripts/bin/
source ${MODELSCRIBES_VENV?}/activate
chmod +x ${MODELSCRIBES_HOME?}/bin/*
chmod +x ${MODELSCRIBES_HOME?}/modelscribes/use/engine/res