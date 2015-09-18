# -*- coding: utf-8 -*-

import datetime
import numpy as np
import csv

from PyQt5.QtCore import QFile
from PyQt5.QtCore import QTextStream
from PyQt5.QtCore import QIODevice

class mWaveFile():

    def __init__(self, filename = None):
        super(mWaveFile, self).__init__()
        self.time = datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
        self.dataWaveLength = []
        self.dataAbs = []
        self.dataTransmittance = []

        self.dataWave = []

        if (filename != None):
            self.filename = filename
            self.loadFile()
            self.parseOutputData()


    def loadFile(self):
            fh = QFile(self.filename)
            print("fh is ",fh)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            #self.setPlainText("Hello World")
            self.preParse = (stream.readAll()) #Here lies the problem how to fix it? PyQt 3.4.2 Works Fine
            print(self.preParse)
            self.parseOutputData(self.preParse)
            #self.outputTextdocument().setModified(False)


    def calcTransmitanceFromAbs(self, absorbance):
        ##%T = (IT/I0)*100.
        ##Absorbance is actually log10 (I0/IT)
        ##100/%T = I0/IT


        ##A = 2 - log10 %T //This is the right formula
        ## - log10 %T = A -2
        ## log10 %T = (2-A)
        ## T = 10**(2-A)
        logT = (2-absorbance)
        transmittance = (10**logT)
        return transmittance




    def parseOutputData(self,fullText = ""):
        #print("Full Text ",fullText)
        fullText = fullText.split("\n")
        #print("Full Text ",fullText)
        for i in fullText:
            temp = i.split(" ")
            #print(temp)
            if ("START WAVELENGTH" in i):
                #print(temp)
                waveLen = float(temp[-1].split('nm')[0])
                self.dataWave.append(waveLen)
            if ("END WAVELENGTH" in i):
                waveLen = float(temp[-1].split('nm')[0])
                self.dataWave.append(waveLen)
            if ("SCAN INTERVAL" in i):
                waveLen = float(temp[-1].split('nm')[0])
                self.dataWave.append(waveLen)

            #print('self.dataWave ', self.dataWave)
            #print('------------------------------')
            temp = i.split(",")
            if len(temp) == 2:
                #print(temp)
                self.dataWaveLength.append(float(temp[0]))
                specData = float(temp[1])
                self.dataAbs.append(specData)
                self.dataTransmittance.append(self.calcTransmitanceFromAbs(specData))

        #print('tada ',len(self.dataWaveLength))



    def saveMWaveFile(self,filename = "none.mls"):
        with open(filename, 'w') as mWave:
            mWave.write('''"M.Wave File"\n''')
            mWave.write('''"Spectrum Scan"\n''')
            mWave.write('''"0"\n''') #Maybe Sample
            mWave.write('''"%s"\n''' %(str(int(self.dataWave[1]))))
            mWave.write('''"%s"\n''' %(str(int(self.dataWave[0]))))
            mWave.write('''"%s"\n''' %(str(int(self.dataWave[2]))))
            mWave.write('''"%s"\n''' %(str(int(self.dataWave[2])))) #This is a ?

            mWave.write('''"%s"\n''' %(self.time))# Time and Date

            mWave.write('''"%s"\n''' %(len(self.dataWaveLength)))# total frames

            mWave.write('''"","","",""\n''' )# total frames

            for i in range(1,len(self.dataWaveLength)+1):
                print(i, self.dataWaveLength[-i], self.dataAbs[-i],self.dataTransmittance[-i]  )
                tempText = '''"%s","%s","%s","%s"\n''' %(i,
                                                        int(self.dataWaveLength[-i]),
                                                        self.dataAbs[-i],
                                                        self.dataTransmittance[-i] )

                mWave.write(tempText)# total frames


            finalText = '''"File End"'''
            mWave.write(finalText)





#rs232File = 'Output_test.rs232'
#mWaveObj = mWaveFile(rs232File )

#saveFileName = 'Output_test.wls'
#mWaveObj.saveMWaveFile(saveFileName)