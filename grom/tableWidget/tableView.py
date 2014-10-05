# -*- coding: utf-8 -*-
"""
    GROM.PDB_tableview
    ~~~~~~~~~~~~~

    Custom  TableView

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

from __future__ import absolute_import

#: Importing from  PyQt5.QtCore
from PyQt5.QtCore import  Qt
from PyQt5.QtCore import QFileInfo

#: Importing from  PyQt5.QtWidgets

from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QFileDialog


try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str

import sys
#from pprint import pprint as pp
#print(pp(sys.path))

from  tableWidget.PDB_parse import *
import tableWidget.pdb_model_0_88 as pdb_model

from  tableWidget.GRO_parse import *
import tableWidget.gro_model as gro_model

from tableWidget.undoCommands import * #CommandRename, CommandAddRow,CommandRemoveRow
import tableWidget.frTableEdit as frTableEdit


def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True




class TableEdit(QTableView):


    def __init__(self, filename= '', modelType = None,parent=None):
        """
        Method defines  Custom QTableView
        Args:
             filename (str) file to oepn if there is any
        """
        super(TableEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent = parent
        #print('parent is ',self.parent)
        self.filename = filename
        self.modelType = modelType
        print("self.filename at start is ",self.filename)
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        self.setStyleSheet("QTableView { background-color: rgb(230, 230, 230);}")

        #: Create Model Instant
        self.setCustomModel()

        self.clicked.connect(self.updateSelectionValues)

        self.undo_Stack = self.delegate.undoStack

        #: Create Search Instance for this Widget
        self.frTableObject = frTableEdit.frTableObject(self)
        self.keylist = []


    def setCustomModel(self):
        if 'pdb' in self.filename or self.modelType == 'PDB':
            self.model = pdb_model.PDBTableModel(self.filename)
            self.setModel(self.model)
            self.delegate = pdb_model.PDBDelegate(self)
            self.setItemDelegate(self.delegate) #
        elif 'gro' in self.filename or self.modelType == 'GRO':
            self.model = gro_model.GROTableModel(self.filename)
            self.setModel(self.model)
            self.delegate = gro_model.GRODelegate(self)
            self.setItemDelegate(self.delegate) #

    def initialLoad(self):
        try:
            self.model.load(self.filename)
            self.frTableObject.rowCount = self.model.rowCount()
            self.model.endResetModel()
            self.model.dirty = False
        except IOError as e:
            QMessageBox.warning(self, "PDB file load  - Error",
                    "Failed to load: {}".format(e))
        self.resizeColumns()

    def resizeColumns(self):
        self.resizeColumnsToContents()



    def editCopy(self):
        self.data_copy= self.buffer_temp()

    #: This function hasn't been implemented yet
    def ResNumFixer(self):
        ''' Need to make comparison between ATOM Names
        '''
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        #print('rows ',rows)
        #print('columns ',cols)
        res_now = 1
        temp_name = self.model.PDB_rows[0].access[2]
        temp_resName = self.model.PDB_rows[0].access[3]
        temp_resNum = self.model.PDB_rows[0].access[5]



    #: Function copies indexes and its values
    def buffer_temp(self): #Needs fixing
        data = []
        for item in self.selectedIndexes():
                row =  int(item.row())
                column = int(item.column())
                color_data = None
                item_val = self.model.getVal(row,column)
                color_data = None
                #if column == 0:
                    #color_data = self.model.PDB_rows[row].ATOM_TextColor
                #elif column == 4:
                    #color_data = self.model.PDB_rows[row].ChainID_color
                #elif column == 5:
                    #color_data = self.model.PDB_rows[row].resNum_color
                data.append([[row,column,item],[item_val,color_data]])
        return data



    def save(self):
        try:
            if 'Untitled' in self.filename:
                filename = QFileDialog.getSaveFileName(self,
                        "GROM Editor -- Save File ", self.filename,
                        "MD files (*.pdb *.gro *.*)")
                if len(filename[0]) == 0:
                    return
                self.filename = filename[0]
                #Now need to extract the data and save it
            self.model.save(self.filename)
        except Exception as e:
            print("Coudn't save ",e)


    def saveAs(self):
        try:
            filename = QFileDialog.getSaveFileName(self,
                    "GROM Editor -- Save File ", self.filename,
                    "MD files (*.pdb *.gro *.*)")
            if len(filename[0]) == 0:
                return
            self.filename = filename[0]
            print('self.filename is ',self.filename)
            #Now need to extract the data and save it
            self.setWindowTitle(QFileInfo(self.filename).fileName())
            self.model.save(self.filename)
        except Exception as e:
            print("Coudn't save ",e)


    def updateSelectionValues(self):
        values = self.selectedIndexes()[0]
        row = values.row()
        column  = values.column()
        self.frTableObject.updateCurrentSelectionDown(row,column)
        self.frTableObject.updateCurrentSelectionUp(row,column)


    def updateToZero(self):
        self.frTableObject.updateCurrentSelectionUp(0,0)
        self.frTableObject.updateCurrentSelectionDown(0,0)

    def setSearchTextValue(self,val1,val2):
        self.frTableObject.setFindVal(val1,val2)

    def getSearchTextValue(self):
        return  self.frTableObject.getFindText()

    def upMove(self):
        self.frTableObject.upSearch()

    def downMove(self):
        self.frTableObject.downSearch()

    def findAll(self,findText):
        self.frTableObject.findAllItems(findText)


    def updateSearchText(self):
        self.frTableObject.updateTextContent()

    def search(self,findText,replaceText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        self.frTableObject.search(findText,replaceText,syntaxCombo)



    def replaceAll(self,findText,replaceAllText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        self.frTableObject.findAllItems(findText)
        indexes = self.selectedIndexes()
        indexes = self.selectedIndexes()
        command = CommandRename(self, self.model, indexes,replaceAllText,
                             "Multirename values")
        self.undo_Stack.push(command)
        self.clearSelection()








    def replace(self,value,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False): #this one needs to add a lot
        indexes = self.selectedIndexes()
        command = CommandRename(self, self.model, indexes,value,
                             "Multirename values")
        self.undo_Stack.push(command)
        self.clearSelection()


    def multi_rename(self,value): #this one needs to add a lot
        indexes = self.selectedIndexes()
        command = CommandRename(self, self.model, indexes,value,
                             "Multirename values",tableAdress = self)
        self.undo_Stack.push(command)

    def editCut(self):
        self.data_copy= self.buffer_temp()
        command = CommandCut(self.model,self.data_copy,'',
                             "Cut value",tableAdress = self)
        self.undo_Stack.push(command)





    def editPaste(self):
        self.to_modify = self.buffer_temp()


        command = CommandPaste(self.model,self.data_copy,self.to_modify,
                             "Paste value",tableAdress = self)
        self.undo_Stack.push(command)

    def getModel(self):
        return self.model




    def undo(self):
        print("undo man")
        self.undo_Stack.undo()


    def redo(self):
        self.undo_Stack.redo()

    def keyPressEvent(self, event):
        self.firstrelease = True
        event_check = int(event.key())
        #event = event.key
        self.keylist.append(event_check)
        #print(self.keylist)
        Key_Control = 16777249
        Shift_Control = 16777248
        if event.key()==( Qt.Key_F1): #It should show if there action not activated
            self.parent.showHelpMenu()
            return
        if Key_Control not in self.keylist:# or  Qt.Key_Shift not in self.keylist:
            #print('Choice 1')
            QTableView.keyPressEvent(self,event)
            return
        #elif Shift_Control not in self.keylist:
            #print('Choice 2')
            #QPlainTextEdit.keyPressEvent(self,event)

    def keyReleaseEvent(self, event):
        try:
            if self.firstrelease == True:
                self.processmultikeys(self.keylist)


            self.firstrelease = False

            del self.keylist[-1]
        except:
            pass

    def processmultikeys(self,keyspressed):
        #print('keysPressed is ',keyspressed)
        if Qt.Key_Control  in keyspressed and Qt.Key_X in keyspressed:
            self.editCut()
        elif (Qt.Key_Control in keyspressed and Qt.Key_C in keyspressed):
            self.editCopy()
        elif (Qt.Key_Control in keyspressed and Qt.Key_V in keyspressed):
            self.editPaste()
        elif (Qt.Key_Control in keyspressed and Qt.Key_N in keyspressed):
            self.parent.chooseNew()
        elif (Qt.Key_Control in keyspressed and Qt.Key_O in keyspressed):
            self.parent.FileOpen()
        elif (Qt.Key_Control in keyspressed and Qt.Key_S in keyspressed):
            self.parent.fileSave()
        elif (Qt.Key_Control in keyspressed and Qt.Key_F in keyspressed):
            self.parent.FindReplace()
        elif (Qt.Key_Control in keyspressed and Qt.Key_H in keyspressed):
            self.parent.FindReplace()
        elif (Qt.Key_Control in keyspressed and Qt.Key_Shift in keyspressed and Qt.Key_A in keyspressed):
            self.clearSelection() #Problem?
        elif (Qt.Key_Control in keyspressed and Qt.Key_A in keyspressed):
            self.selectAll()
        elif (Qt.Key_Control in keyspressed and Qt.Key_Shift in keyspressed and Qt.Key_Z in keyspressed):
            #print("redo Working")
            self.redo()
        elif (Qt.Key_Control in keyspressed and Qt.Key_Z in keyspressed):
            #print("undo working")
            self.undo()
        elif (Qt.Key_Control in keyspressed and Qt.Key_R in keyspressed): #THis is problematic
            self.parent.MultiRename() #Multiple Rename

    def  AddRow(self,rows):
        command = CommandAddRow(self, self.model, rows,
                             "Add Row")
        self.undo_Stack.push(command)


    def RemoveRow(self,rows):
        command = CommandRemoveRow(self, self.model, rows,
                             "Remove Row")
        self.undo_Stack.push(command)
        #self.resizeColumns()