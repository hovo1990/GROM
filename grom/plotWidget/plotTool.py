# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
    GROM.plotTool
    ~~~~~~~~~~~~~

    This is the main program with its GUI

    :copyright: (c) 2015 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

from __future__ import absolute_import



import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure





#: Import from PyQt5.QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QFileInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import QTextStream


#: Import from PyQt5.QtQtGui
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QTextFormat
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QPalette

#: Import from PyQt5.QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import (pyqtProperty, pyqtSignal)





class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
          pass

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class plotWidget(QWidget):

    NextId = 1

    FONT_MAX_SIZE = 30
    FONT_MIN_SIZE = 10

    TEXTCHANGED = 0

    customDataChanged = pyqtSignal()

    def __init__(self, filename= None, parent=None):
        """
        Creates an Instance of QPlainTextEdit

         Args:
             filename (str): for opening a parameter file
             parent  (object)

        """
        super(plotWidget, self).__init__(parent)
        self.parent = parent

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.filename = filename #VIT
        self.setWindowTitle(QFileInfo(self.filename).fileName())

        l = QVBoxLayout(self)
        sc = MyStaticMplCanvas(self, width=5, height=4, dpi=100)
        l.addWidget(sc)



