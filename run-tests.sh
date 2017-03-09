#!/bin/bash -e

pyuic5 src/pesel2pbn/pesel2pbn.ui >  src/pesel2pbn/pesel2pbn_auto.py

export PYTHONPATH=".:.."
py.test src/pesel2pbn/tests.py