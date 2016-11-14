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
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
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


def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a


def relative_strength(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi


def moving_average_convergence(x, nslow=26, nfast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = moving_average(x, nslow, type='exponential')
    emafast = moving_average(x, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        # self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class showPlot(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def plotFigure(self, x, y, xlabel, ylabel, title):
        self.x = x
        self.y = y
        self.axes.plot(self.x, self.y)
        # self.axes.subplot(211)
        # ma20 = moving_average(self.y, 50, type='simple') #
        # self.axes.plot(self.x, ma20)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.draw()
        # FigureCanvas.updateGeometry(self)

    def saveFig(self, saveFilename):
        print('saveName ', saveFilename)
        try:
            self.fig.savefig(saveFilename)
        except Exception as e:
            print("Error in saving figure ", e)


class plotWidget(QWidget):
    NextId = 1

    FONT_MAX_SIZE = 30
    FONT_MIN_SIZE = 10

    TEXTCHANGED = 0

    customDataChanged = pyqtSignal()

    def __init__(self, filename=None, parent=None):
        """
        Creates an Instance of QWidget

         Args:
             filename (str): for opening a parameter file
             parent  (object)

        """
        super(plotWidget, self).__init__(parent)
        self.parent = parent

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.filename = filename  # VIT
        self.save_title = ''

        self.setWindowTitle(QFileInfo(self.filename).fileName())

        hbox = QHBoxLayout(self)
        self.plotToolWidget = showPlot(self, width=5, height=4, dpi=100)

        self.listWidget = QListWidget(self)
        self.listWidget.currentRowChanged.connect(self.updatePlot)
        # self.listWidget.setMinimumWidth(200)
        self.listWidget.setMaximumWidth(200)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)  # This is Yeah
        self.splitter.addWidget(self.plotToolWidget)  # This is Yeah
        self.splitter.addWidget(self.listWidget)  # This is Yeah

        hbox.addWidget(self.splitter)
        # hbox.addWidget(listWidget)

        self.readData()

    def updatePlot(self):
        print("Update Plot Yahooooo ")
        row = self.listWidget.currentRow()
        self.title = self.listWidget.item(row).text()
        print('Row ', row)
        print('----------------------------')
        x, y = self.edrObject.dataExtractFromRow(row)
        unit = self.edrObject.getUnits(row)
        print('Unit is ', unit)
        # print('x ',len(x))
        # print('y ',len(y))

        self.plotToolWidget.plotFigure(x, y, 'ps', unit, self.title)

    def readData(self):
        self.edrObject = EdrIO(self.filename, 'float')  # for now
        print('edrObject ', self.edrObject)
        self.populateList()

    def populateList(self):
        self.props = self.edrObject.read('avail quantities')
        print('props ', self.props)
        index = 0
        for i in self.props:
            self.listWidget.addItem(str(index) + '. ' + i)
            index += 1

    def save(self):
        #: So self.title has to be modified
        self.save_title = self.title.split(' ')[1] + '.png'
        print('save_title is ', self.save_title)

        if "edr" in self.filename:
            filename = QFileDialog.getSaveFileName(self,
                                                   "G.R.O.M. Editor -- Save File As", self.save_title,
                                                   "png (*.png  *.*)")
            print('filename is ', filename)
            if len(filename[0]) == 0:
                return
            self.filenameSave = filename[0]
            print('Save graph ', self.filenameSave)
        # self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            # fh = QFile(self.filenameSave)
            # if not fh.open(QIODevice.WriteOnly):
            # raise IOError(str(fh.errorString()))
            self.plotToolWidget.saveFig(self.filenameSave)
        except EnvironmentError as e:
            exception = e
            print('error in saving ', e)
            # finally:
            # if fh is not None:
            # fh.close()
            # if exception is not None:
            # raise exception
            #
