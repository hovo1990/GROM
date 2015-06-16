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
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import  QMainWindow
from PyQt5.QtWidgets import  QMenu
from PyQt5.QtWidgets import  QHBoxLayout
from PyQt5.QtWidgets import  QSizePolicy
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtWidgets import  QWidget
from PyQt5.QtWidgets import QListWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from PyQt5 import QtCore, QtGui, QtWidgets


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

from .edrParse import *



class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        #self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
          pass

class showPlot(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def plotFigure(self,x, y):
        self.x = x
        self.y = y
        self.axes.plot(self.x, self.y)
        self.draw()
        #FigureCanvas.updateGeometry(self)



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
        Creates an Instance of QWidget

         Args:
             filename (str): for opening a parameter file
             parent  (object)

        """
        super(plotWidget, self).__init__(parent)
        self.parent = parent

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.filename = filename #VIT





        self.setWindowTitle(QFileInfo(self.filename).fileName())

        hbox = QHBoxLayout(self)
        self.plotToolWidget = showPlot(self, width=5, height=4, dpi=100)

        self.listWidget = QListWidget(self)
        self.listWidget.currentRowChanged.connect(self.updatePlot)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal) #This is Yeah
        self.splitter.addWidget(self.plotToolWidget)  #This is Yeah
        self.splitter.addWidget(self.listWidget) #This is Yeah

        hbox.addWidget(self.splitter)
        #hbox.addWidget(listWidget)

        self.readData()

    def updatePlot(self):
        print("Update Plot Yahooooo ")
        row = self.listWidget.currentRow()
        print('Row ',row)
        print('----------------------------')
        x,y = self.edrObject.dataExtractFromRow(row)
        #print('x ',len(x))
        #print('y ',len(y))
        self.plotToolWidget.plotFigure(x,y)

    def readData(self):
        self.edrObject = EdrIO(self.filename, 'float') #for now
        print('edrObject ', self.edrObject)
        self.populateList()

    def populateList(self):
        self.props = self.edrObject.read('avail quantities')
        print('props ',self.props)
        for i in self.props:
            self.listWidget.addItem(i)

