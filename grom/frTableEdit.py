# -*- coding: utf-8 -*-
"""
    GROM.frTableEdit
    ~~~~~~~~~~~~~

    This is the Search Object for TableWidget

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""


import re
from PyQt5.QtCore import (Qt,QItemSelectionModel)
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QWidget, QMessageBox)
import undoCommands


try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str


class frTableObject(QWidget):

    def __init__(self,tableEditorAddress,parent = None):
        """
        Method defines  Search Object for Table Widget

        Args:
             tableEditorAddress (QWidget*) Reference Address for tableWidget
        """
        super(frTableObject, self).__init__(parent)
        self.__tableEditor = tableEditorAddress
        self.model = self.__tableEditor.getModel()

        self.rowCount = self.model.rowCount()
        self.columnCount = 12
        #print('tableEditorAddress is ',self.__tableEditor)



        self.__findText = ''
        self.__replaceText = ''


        self.found = False
        self.__index = 0

        self.__currentSelectionUp = [0,0]
        self.__currentSelectionDown = [0,0]


    def addTableSearch(self,row,column):
        self.rowToSearchAfter = row
        self.columnToSearchAfter = column

    def setFindVal(self,val1,val2):
        self.__findText = val1
        self.__replaceText = val2

    def getFindText(self):
        return [self.__findText,self.__replaceText]


    def updateCurrentSelectionDown(self,val1,val2):
        self.__currentSelectionDown = [val1,val2]

    def updateCurrentSelectionUp(self,val1,val2):
        self.__currentSelectionUp = [val1,val2]

    def upSearch(self): #Need to work this out
        try:
            for row in range(self.__currentSelectionUp[0],-1,-1):
                for column in range(self.__currentSelectionUp[1],-1,-1):
                    index = self.model.index(row, column)
                    pattern = r"%s" %str((self.__findText))
                    item = r"%s" %(str(self.model.data(index)))
                    match = self.searchObj(pattern,item)
                    if column == 0 and row == 0 and  match == False:
                        index = self.model.index(0, 0)
                        self.selectItems(index)
                        QMessageBox.warning(self,"Oops",'Found nothing')
                        self.updateCurrentSelectionDown(0,0)
                        self.updateCurrentSelectionUp(0,0)
                        return
                    if column == 0 and match == False:
                        #print('selection row is ',self.__currentSelection[0])
                        row = self.__currentSelectionUp[0]
                        column = 11
                        self.updateCurrentSelectionUp(row-1,column)
                        self.updateCurrentSelectionDown(row,0)
                    if match == True:
                        if index.row() == self.__currentSelectionUp[0]:
                            self.selectItems(index)
                            self.__currentSelectionUp = [row,column-1]
                            self.__currentSelectionDown = [row,column+1]
                            #print('current selection ',self.__currentSelection)
                            return
        except Exception as e:
            print("Duh Up search ",e)



    def searchObj(self,pattern, string):
        searchObj = re.search(pattern,string, re.I)
        try:
            if searchObj.group():
                return True
            else:
                return False
        except:
            return False

    def downSearch(self): #this is a better version
        try:
            for row in range(self.__currentSelectionDown[0],self.rowCount):
                for column in range(self.__currentSelectionDown[1],self.columnCount):
                    index = self.model.index(row, column)
                    pattern = r"%s" %str((self.__findText))
                    item = r"%s" %(str(self.model.data(index)))
                    match = self.searchObj(pattern,item)
                    if column >= 11 and row == self.rowCount-1 and  match == False:
                        index = self.model.index(0, 0)
                        self.selectItems(index)
                        QMessageBox.warning(self,"Oops",'Found nothing')
                        self.updateCurrentSelectionDown(0,0)
                        self.updateCurrentSelectionUp(0,0)
                        return
                    if column >= 11 and match == False:
                        #print('selection row is ',self.__currentSelection[0])
                        row = self.__currentSelectionDown[0]
                        column = 0
                        self.updateCurrentSelectionDown(row+1,column)
                        self.updateCurrentSelectionUp(row,11)
                    if match == True:
                        #print('index is ',index)
                        if index.row() == self.__currentSelectionDown[0]:
                            self.selectItems(index)
                            self.__currentSelectionDown = [row,column+1]
                            self.__currentSelectionUp = [row,column-1]
                            return
        except Exception as e:
            print("Duh down search ",e)


    def selectItems(self,index):
        try:
            self.__tableEditor.clearSelection()
            self.__tableEditor.selectionModel().select(
                    index, QItemSelectionModel.Select)
            self.__tableEditor.scrollTo(index)
        except Exception as e:
            print('selectItems error  is ',e)





    def selectAllItems(self,index):
        try:
            self.__tableEditor.selectionModel().select(
                    index, QItemSelectionModel.Select)
            self.__tableEditor.scrollTo(index)
        except Exception as e:
            print('selectAllItmes error  is ',e)



    def findAllItems(self,searchVal):
        try:
            self.__rowSearchDown = 0
            self.__rowSearchUp = 0
            self.__columnSearchDown = 0
            self.__columnSearchUp = 0
            self.__tableEditor.clearSelection()
            self.__findText = searchVal
            for i in range(12):
                start = self.model.index(0, i)
                matches = self.model.match(
                    start, Qt.DisplayRole,
                    self.__findText, -1, Qt.MatchContains)
                if matches:
                    for i in matches:
                        self.selectAllItems(i)
        except Exception as e:
            print("Duh findALLsearch ",e)


    def search(self,findText,replaceText = None,syntaxCombo = None):
        if self.found  == True:
            self.fixFormat()
        self.__index = 0
        self.__findText = findText
        self.resFoundText = []
        findText = findText
        if len(findText) < 1:
            self.fixFormat()
        else:
            regex = self.makeRegex(findText,syntaxCombo)
            while True:
                match = regex.search(self.__text, self.__index)                  # look here
                if match is  None:
                    self.found = True
                    break
                else:
                    self.resFoundText.append([match.start(),match.end()])
                    self.__index = match.end()
                    self.highlightText(findText,match.start())
        self.returnToStart()



    def on_findButton_clicked(self):
            findText = str(self.findLineEdit.text())
            self.findInTable(findText,self.rowToSearchAfter,self.columnToSearchAfter)


    def findInTable(self,text,row ,column):
        print("before row is %s  column is %s" %(row,column))
        model = self.__table.getModel()
        start = model.index(row, column)
        matches = model.match(
            start, Qt.DisplayRole,
            text, 1, Qt.MatchContains)
        if matches:
            index = matches[0]
            row = index.row() +1
            column = index.column()

