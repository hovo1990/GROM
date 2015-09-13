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



from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal



try:
    from PyQt5.QtCore import QString
except ImportError:
     #we are using Python3 so QString is not defined
    QString = str


import matplotlib.pyplot as plt
import numpy as np
import csv

import sys, serial
from  .rs232Skeleton import Ui_Form #Imports MainWindow GUI


#newDataSignal = pyqtSignal(QString , name = "newData" )
#errorMsgSignal = pyqtSignal(QString , name = "error" )



class rs232Widget(QWidget, Ui_Form):

    NextId = 1

    FONT_MAX_SIZE = 30
    FONT_MIN_SIZE = 10

    TEXTCHANGED = 0

    #customDataChanged = pyqtSignal()

    newDataSignal = pyqtSignal(QString , name = "newData" )
    errorMsgSignal = pyqtSignal(QString , name = "error" )
    finishedSignal = pyqtSignal(QString , name = "finished" )


    def __init__(self, filename= None, parent=None):
        """
        Creates an Instance of QWidget

         Args:
             filename (str): for opening a parameter file
             parent  (object)

        """
        super(rs232Widget, self).__init__(parent)
        self.parent = parent
        self.reader = CReader(self.newDataSignal,self.errorMsgSignal, self.finishedSignal)
        self.writer = CWriter(self.newDataSignal,self.errorMsgSignal)
        self.setupRealUi()

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.filename = filename #VIT
        if (self.filename) != '':
            self.loadRS232File()
            self.parseData()


        self.save_title = ''
        self.ser = None #Testing



    def parseData(self): #Yolo
        self.dataX = []
        self.dataY = []
        fullText = self.outputText.toPlainText()
        #print("Full Text ",fullText)
        fullText = fullText.split("\n")
        #print("Full Text ",fullText)
        for i in fullText:
            temp = i.split(",")
            if len(temp) == 2:
                #print(temp)
                self.dataX.append(float(temp[0]))
                self.dataY.append(float(temp[1]))


    def plotResults(self):
        print('what is the problem darn')
        dataX = np.array(self.dataX)
        dataY = np.array(self.dataY)
        plt.plot(dataX, dataY)
        plt.show()


    def saveCSVFile(self):
        filename = QFileDialog.getSaveFileName(self,
                "G.R.O.M. Editor -- Save File As", self.filename,
                "CSV (*.csv *.*)")
        print('filename is ',filename)
        if len(filename[0]) == 0:
            return
        self.filenameCSV = filename[0]
        with open(self.filenameCSV, 'w') as csvfile:
            fieldnames = ['Wave', 'Absorption']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for x,y in zip(self.dataX, self.dataY):
                writer.writerow({'Wave': x, 'Absorption': y})
            #writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
            #writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            #writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

    def saveRS232File(self):
        #if "Unnamed" in self.filename:
        filename = QFileDialog.getSaveFileName(self,
                "G.R.O.M. Editor -- Save File As", self.filename,
                "RS232 (*.rs232 *.*)")
        print('filename is ',filename)
        if len(filename[0]) == 0:
            return
        self.filename = filename[0]
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.outputText.toPlainText()
            #self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception



    def loadRS232File(self): #Windows crash buty why
        exception = None
        fh = None


        print("Hello Load Text File")
        #Looks like there's bug in windows
        try:
            fh = QFile(self.filename)
            print("fh is ",fh)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            #self.setPlainText("Hello World")
            self.outputText.setPlainText(stream.readAll()) #Here lies the problem how to fix it? PyQt 3.4.2 Works Fine
            #self.outputTextdocument().setModified(False)
        except EnvironmentError as e:
            exception = e
            print("Exception is ",exception)




    def setupRealUi(self):
        self.setupUi(self)

        self.connectButton.clicked.connect(self.connectToDevice)
        self.disconnectButton.clicked.connect(self.disconnectFromDevice)
        self.commandSendButton.clicked.connect(self.sendCommandToDevice)

        self.saveOutputButton.clicked.connect(self.saveRS232File) #For Saving File
        self.exportCSVButton.clicked.connect(self.saveCSVFile)
        self.plotButton.clicked.connect(self.plotResults)


        #self.reader.newData.connect(self.updateLog)
        self.newDataSignal.connect(self.updateLog)
        self.errorMsgSignal.connect(self.updateLog)
        #self.finishedSignal.connect(self.parseData)





    def sendCommandToDevice(self):
        cmd = self.commandEdit.text()
        self.printCmd(cmd)
        self.writer.start(self.ser, cmd)
        self.commandEdit.clear()

    def connectToDevice(self):
          self.disconnectFromDevice()
          print("What the hell is ")
          try:

             portName = self.getPortName()
             print("portName" ,portName)
             baudRate = self.getBaudRate()
             print("baudRate ",baudRate)
             byteSize = self.getByteSize()
             print("byteSize ",byteSize)
             parityType = self.getParityType()
             print("parityType ",parityType)
             stopBits  = self.getStopBits()
             print("stopBits ",parityType)
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
          except Exception as e:
             self.ser = None
             self.printError("Failed to connect!")
             self.print("Error ",e)


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
        print("value is ",value)
        if value == "Odd":
            returnVal  = serial.PARITY_ODD
        return returnVal

    def getStopBits(self):
        value = self.stopBitsSpinBox.value()
        if value == 2:
            returnVal = serial.STOPBITS_TWO
        elif value == 1:
            returnVal = serial.STOPBITS_ONE
        return returnVal


    def startReader(self, ser):
        self.reader.start(ser) #VIP

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


    @QtCore.pyqtSlot(QString)
    def updateLog(self, text):
         self.outputText.moveCursor(QTextCursor.End)
         self.outputText.insertPlainText(text)
         self.outputText.moveCursor(QTextCursor.End)
         if "END OF POST SCAN DATA" in self.outputText.toPlainText():
             self.parseData()

    def closeEvent(self, event):
        self.disconnect()



class CReader(QThread):

   def __init__(self,newDataSignal,errorMsgSignal,finishedSignal):
      super(CReader, self).__init__()
      self.newDataSignal = newDataSignal
      self.errorMsgSignal = errorMsgSignal
      self.finishedSignal = finishedSignal



   def start(self, ser, priority = QThread.InheritPriority):
       self.ser = ser
       QThread.start(self, priority)

   def run(self):
      while True:
         try:
            data = self.ser.read(1).decode("ascii")
            #print("dataRead is ",data)
            n = self.ser.inWaiting()
            if n:
               data = data + self.ser.read(n).decode("ascii")
            #self.emit(SIGNAL("newData(QString)"), data)
            self.newDataSignal.emit(data) #Here lies the problem
         except:
            errMsg = "Reader thread is terminated unexpectedly."
            #self.emit(SIGNAL("error(QString)"), errMsg)
            #errorMSG
            self.errorMsgSignal.emit(errMsg)
            break

class CWriter(QThread):

   def __init__(self,newDataSignal,errorMsgSignal):
      super(CWriter, self).__init__()
      self.newDataSignal = newDataSignal
      self.errorMsgSignal = errorMsgSignal




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
         #self.emit(SIGNAL("error(QString)"), errMsg)
         self.errorMSG.emit(errMsg)

   def terminate(self):
      self.wait()
      QThread.terminate(self)


