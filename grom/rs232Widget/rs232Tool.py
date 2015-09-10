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
from PyQt5.QtCore import QThread
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


import sys, serial
from  .rs232Skeleton import Ui_Form #Imports MainWindow GUI


class rs232Widget(QWidget, Ui_Form):

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
        super(rs232Widget, self).__init__(parent)
        self.parent = parent

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.filename = filename #VIT
        self.save_title = ''
        self.ser = None #Testing


        self.reader = CReader()
        self.writer = CWriter()
        self.setupRealUi()


    def setupRealUi(self):
        self.setupUi(self)

        self.connectButton.clicked.connect(self.connectToDevice)
        self.disconnectButton.clicked.connect(self.disconnectFromDevice)
        self.commandSendButton.clicked.connect(self.sendCommandToDevice)



    def sendCommandToDevice(self):
        cmd = self.commandEdit.text()
        self.printCmd(cmd)
        self.writer.start(self.ser, cmd)
        self.self.commandEdit.clear()

    def connectToDevice(self):
          self.disconnectFromDevice()
          try:

             portName = self.getPortName()
             baudRate = self.getBaudRate()
             byteSize = self.getByteSize()
             parityType = self.getParityType()
             stopBits  = self.getStopBits()
             self.printInfo("Connecting to %s with %s baud rate." % \
                            (portName, baudRate))
             self.ser = serial.Serial(  port=str(portName),
                                        baudrate=baudRate,
                                        parity=parityType,
                                        stopbits=stopBits,
                                        bytesize= byteSize
                                       )
             self.startReader(self.ser)
             self.printInfo("Connected successfully.")
          except:
             self.ser = None
             self.printError("Failed to connect!")


    def disconnectFromDevice(self):
          self.stopThreads()
          if self.ser == None: return
          try:
             if self.ser.isOpen:
                self.ser.close()
                self.printInfo("Disconnected successfully.")
          except:
             self.printError("Failed to disconnect!")
          self.ser = None


    def getPortName(self):
      return self.portName.text()

    def getBaudRate(self):
        return self.baudrateSpinbox.value()

    def getByteSize(self):
        value = self.bytesizeSpinbox.value()
        if value == 7:
            returnVal = serial.SEVENBITS
        return  returnVal

    def getParityType(self):
        value = self.parityComboBox.currentText()
        if value == "odd":
            returnVal  = serial.PARITY_ODD
        return returnVal

    def getStopBits(self):
        value = self.stopBitsSpinBox.value()
        if value == 2:
            returnVal = serial.STOPBITS_TWO
        return returnVal


    def startReader(self, ser):
        self.reader.start(ser)

    def stopThreads(self):
          self.stopReader()
          self.stopWriter()

    def stopReader(self):
          if self.reader.isRunning():
              self.reader.terminate()

    def stopWriter(self):
          if self.writer.isRunning():
             self.writer.terminate()

    def printInfo(self, text):
          self.outputText.appendPlainText(text)
          self.outputText.moveCursor(QTextCursor.End)


    def printError(self, text):
          self.outputText.appendPlainText(text)
          self.outputText.moveCursor(QTextCursor.End)


    def printCmd(self, text):
          self.outputText.appendPlainText("> " + text + "\n\n")
          self.outputText.moveCursor(QTextCursor.End)


    def updateLog(self, text):
         self.outputText.moveCursor(QTextCursor.End)
         self.outputText.insertPlainText(text)
         self.outputText.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        self.disconnect()



class CReader(QThread):

   def start(self, ser, priority = QThread.InheritPriority):
      self.ser = ser
      QThread.start(self, priority)

   def run(self):
      while True:
         try:
            data = self.ser.read(1)
            n = self.ser.inWaiting()
            if n:
               data = data + self.ser.read(n)
            self.emit(SIGNAL("newData(QString)"), data)
         except:
            errMsg = "Reader thread is terminated unexpectedly."
            self.emit(SIGNAL("error(QString)"), errMsg)
            break

class CWriter(QThread):

   def start(self, ser, cmd = "", priority = QThread.InheritPriority):
      self.ser = ser
      self.cmd = cmd
      QThread.start(self, priority)

   def run(self): #Here it has to be modified for Python 3
      try:
         data = bytearray(self.cmd,'ascii')
         self.ser.write(data)
         #self.ser.write(str(self.cmd))
      except:
         errMsg = "Writer thread is terminated unexpectedly."
         self.emit(SIGNAL("error(QString)"), errMsg)

   def terminate(self):
      self.wait()
      QThread.terminate(self)


        #self.setWindowTitle(QFileInfo(self.filename).fileName())

        #hbox = QHBoxLayout(self)
        #self.plotToolWidget = showPlot(self, width=5, height=4, dpi=100)

        #self.listWidget = QListWidget(self)
        #self.listWidget.currentRowChanged.connect(self.updatePlot)
        ##self.listWidget.setMinimumWidth(200)
        #self.listWidget.setMaximumWidth(200)

        #self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal) #This is Yeah
        #self.splitter.addWidget(self.plotToolWidget)  #This is Yeah
        #self.splitter.addWidget(self.listWidget) #This is Yeah

        #hbox.addWidget(self.splitter)
        ##hbox.addWidget(listWidget)

        #self.readData()

    #def updatePlot(self):
        #print("Update Plot Yahooooo ")
        #row = self.listWidget.currentRow()
        #self.title = self.listWidget.item(row).text()
        #print('Row ',row)
        #print('----------------------------')
        #x,y = self.edrObject.dataExtractFromRow(row)
        #unit = self.edrObject.getUnits(row)
        #print('Unit is ',unit)
        ##print('x ',len(x))
        ##print('y ',len(y))

        #self.plotToolWidget.plotFigure(x,y, 'ps', unit, self.title)

    #def readData(self):
        #self.edrObject = EdrIO(self.filename, 'float') #for now
        #print('edrObject ', self.edrObject)
        #self.populateList()

    #def populateList(self):
        #self.props = self.edrObject.read('avail quantities')
        #print('props ',self.props)
        #index = 0
        #for i in self.props:
            #self.listWidget.addItem(str(index) + '. ' +i)
            #index += 1


    #def save(self):
        ##: So self.title has to be modified
        #self.save_title  = self.title.split(' ')[1] + '.png'
        #print('save_title is ',self.save_title)

        #if "edr" in self.filename:
            #filename = QFileDialog.getSaveFileName(self,
                    #"G.R.O.M. Editor -- Save File As", self.save_title,
                    #"png (*.png  *.*)")
            #print('filename is ',filename)
            #if len(filename[0]) == 0:
                #return
            #self.filenameSave = filename[0]
            #print('Save graph ',self.filenameSave)
        ##self.setWindowTitle(QFileInfo(self.filename).fileName())
        #exception = None
        #fh = None
        #try:
            ##fh = QFile(self.filenameSave)
            ##if not fh.open(QIODevice.WriteOnly):
                ##raise IOError(str(fh.errorString()))
            #self.plotToolWidget.saveFig(self.filenameSave)
        #except EnvironmentError as e:
            #exception = e
            #print('error in saving ',e)
        ##finally:
            ##if fh is not None:
                ##fh.close()
            ##if exception is not None:
                ##raise exception
##