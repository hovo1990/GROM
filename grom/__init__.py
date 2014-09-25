# -*- coding: utf-8 -*-
#
# This file is part of GROM.
#
# GROM is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# GROM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GROM; If not, see <http://www.gnu.org/licenses/>.




###############################################################################
# METADATA
###############################################################################

__prj__ = "GROM"
__author__ = "Hovakim Grabski"
__mail__ = "johnwo1990@hotmail.com, hovakim_grabski@yahoo.com, johngra1990@gmail.com"
__source__ = "https://github.com/hovo1990/GROM"
__version__ = "0.5-alpha"
__license__ = "GPL3"

###############################################################################
# DOC
###############################################################################

"""GROM is Text and Table Editor for GROMACS(.itp,.top,.mdp) and
"""


"""
GROM
-----

GROM is a GROMACS(mdp,itp,top) and PDB Editor in one package  based on Qt5,PyQt5 and Python3.
It's GPL licensed!(See LICENSE)


Before you run it:
`````````````````

    Please Install Qt5, Pyqt5 and Python3:
        On Ubuntu:
            sudo apt-get install build-essential
            sudo apt-get install python3
            sudo apt-get install qt5-default qttools5-dev-tools
            sudo apt-get install python3-pyqt5

And run it:

.. code:: bash
    $ python3 GROM.py

"""
###############################################################################
# IMPORTS
###############################################################################

import sys
from PyQt5.QtWidgets import QApplication

#: for cx_freeze
import PyQt5.QtNetwork
import PyQt5.QtWebKit
#import PyQt5.QtPrintSupport
sys.path.append('grom/')
import MainApp

#import sys
#from os.path import join, dirname
#__path__.append(join(dirname(__file__), sys.platform))

###############################################################################
# MAIN
###############################################################################


def setup_and_run():
    """Load the Core module and trigger the execution."""
    # import only on run
    app = QApplication(sys.argv)
    form = MainApp.MainWindow()
    form.show()
    app.exec_()



