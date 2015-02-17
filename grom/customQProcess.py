# -*- coding: utf-8 -*-
import os
import sys




try:
    from PySide import QtCore
    from PySide import QtWidgets
except:
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5 import QtCore
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import QProcess, QTimer
    from PyQt5.QtCore import QObject
    from PyQt5.QtCore import QTime, QTimer


class CustomQProcess(QProcess):

      def __init__(self):
           #Call base class method
           QProcess.__init__(self)
           self.setProcessChannelMode(QProcess.MergedChannels)

           #self.data = []
           #self.final_data = None

           #self.readyReadStandardOutput.connect(self.readStdOutput)
           self.finished.connect(self.killProcess)

      #Define Slot Here
      #@pyqtSlot()
      def readStdOutput(self):
          self.res = str(self.readAllStandardOutput())
          #print(res)
          #test = self.res.split("\\n")
          self.parseOutput(self.res)

      def parseOutput(self, res):
          #print('res is ',res) #Need to parse this down
          temp = res.split("%")
          #print('shit ',temp)
          temp2 = temp[0].split('[')
          #print('fuck temp2 ',temp2)
          self.final_data = temp2[1]
          #return self.final_data
          #print('buhahah ',self.final_data)


      #def getData(self):
          #return self.final_data #Shit there's a problem'


      def killProcess(self):

            self.kill()

