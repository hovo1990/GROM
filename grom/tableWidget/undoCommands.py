# -*- coding: utf-8 -*-
"""
    GROM.undoCommands
    ~~~~~~~~~~~~~

    This is the undoCommands for the main Program

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""


import operator

#: Importing from  PyQt5.QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QItemSelectionModel

#: Importing from  PyQt5.QtWidgets
from PyQt5.QtWidgets import QUndoCommand
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QMessageBox



def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

(ATOM, serial, name, resName,
 ChainID, resNum,X,Y,Z, occupancy, charge, element) = range(12)

class CommandPaste(QUndoCommand): #this is gonna a lot  tougher

    def __init__(self, model,data_copy, modify,description,tableAdress = None): #I've got an Idea
        """
        Method defines Paste function for table Widget
        Args:
             model (QModel*):
             data_copy (list [Row,Column, QIndex][Value]): data_copy
             modfiy ((list [Row,Column, QIndex][Value]): data_copy ) cells to modify
             description (str) description of the Process
             tableAddress (QWidget*) TableWidget Reference
        """
        super(CommandPaste, self).__init__(description)
        self.model= model
        self.tableAdress = tableAdress
        self.data_copy = data_copy
        self.to_modify = modify
        if len(self.data_copy) > 0:
            if len(self.data_copy) >= len(self.to_modify):
                self.to_run = range(len(self.to_modify))
            else:
                self.to_run = range(len(self.data_copy))

    def redo(self):
         for ind in self.to_run: #take care of this
            row = self.to_modify[ind][0][0]
            column = self.to_modify[ind][0][1]
            index = self.to_modify[ind][0][2]
            try:
                item = self.data_copy[ind][1][0]
                self.model.setData(index,item)
                self.selectItems(index)
            except:
                QMessageBox.warning(None,"Oops","You can't copy")


    def selectItems(self,index):
        try:
                #print('found in Coord activated')
                self.tableAdress.clearSelection()
                self.tableAdress.selectionModel().select(
                        index, QItemSelectionModel.Select)
                #self.__tableEditor.scrollTo(index)
        except Exception as e:
            print('Paste error ',e)


    def undo(self):
         for ind in self.to_run: #take care of this
            #row = self.to_modify[ind][0][0]
            #column = self.to_modify[ind][0][1]
            index = self.to_modify[ind][0][2]
            item = self.to_modify[ind][1][0]
            self.model.setData(index,item)
            self.selectItems(index)





class CommandCut(QUndoCommand): #this is gonna a lot  tougher

    def __init__(self,model,buffer_data,cut_val,description,tableAdress = None): #I've got an Idea
        """
        Method defines Cut function for table Widget
        Args:
             model (QModel*):
             buffer_copy (list [Row,Column, QIndex][Value]): data_copy
             cut (str) ''
             description (str) description of the Process
             tableAddress (QWidget*) TableWidget Reference
        """
        super(CommandCut, self).__init__(description)
        print("Cut has been called")
        self.model= model
        self.tableAdress = tableAdress
        self.buffer_data = buffer_data

    def undo(self):
        for ind in self.buffer_data[:]:
            #row = ind[0][0]
            #column = ind[0][1]
            #print('ind is ',ind)
            index = ind[0][2]
            item = ind[1][0]
            self.model.setData(index,item)
            self.selectItems(index)


    def selectItems(self,index):
        try:
                #print('found in Coord activated')
                self.tableAdress.clearSelection()
                self.tableAdress.selectionModel().select(
                        index, QItemSelectionModel.Select)
                #self.__tableEditor.scrollTo(index)
        except Exception as e:
            print('Cut error ',e)



    def redo(self):
        #print("redo called but why")
        for ind in self.buffer_data[:]:
                #print ind[0]
                #row = ind[0][0]
                #column = ind[0][1]
                #item = QTableWidgetItem('')
                #print('fucskskds ',self.model.PDB_rows[row].access[column])
                try:

                    self.model.setData(ind[0][2],'')
                except:
                    self.model.setData(ind[0][2],0)
                self.selectItems(ind[0][2])



class CommandElementChange(QUndoCommand): #this is gonna a lot  tougher

    def __init__(self, parent, editor,model,index,description): #I've got an Idea
        super(CommandElementChange, self).__init__(description)
        self.parent = parent
        self.editor = editor
        self.model= model
        self.index = index
        self.undo_value = index.model().data(index, Qt.DisplayRole)
        self.first_time = True



    def undo(self):
        self.model.setData(self.index,self.undo_value)
        self.model.dataChanged.emit(self.index,self.index)


    def redo(self):
        if self.first_time == True:
            QStyledItemDelegate.setModelData(self.parent, self.editor, self.model, self.index) #this is very important this is the one that changes the text
            self.redo_value = self.index.model().data(self.index, Qt.DisplayRole)
            self.first_time = False
        elif self.first_time == False:
            self.model.setData(self.index,self.redo_value)
        self.model.dataChanged.emit(self.index,self.index)



class CommandRename(QUndoCommand): #this is gonna be tough

    def __init__(self, parent, model, indexes, value,description,tableAdress = None): #I've got an Idea
        """
        Method defines  Rename function for table Widget
        Args:
             parent ()
             model (QModel*): Model reference for table
             index (list [QIndex]): selected Indexes in table
             value (str) Replace all cells with a value
             description (str) description of the Process
             tableAddress (QWidget*) TableWidget Reference
        """
        super(CommandRename, self).__init__(description)
        self.parent = parent
        self.model= model
        self.indexes = indexes
        self.prev_values = []
        self.value = value
        self.tableAdress = tableAdress


    def selectItems(self,index):
        try:
            #print('found in Coord activated')
            self.tableAdress.clearSelection()
            self.tableAdress.selectionModel().select(
                    index, QItemSelectionModel.Select)
            self.tableAdress.scrollTo(index)
        except Exception as e:
            print('Rename error ',e)

    def redo(self):
        for index in self.indexes:
            temp_undoValue = index.model().data(index, Qt.DisplayRole)
            self.prev_values.append(temp_undoValue)
            self.model.setData(index,self.value)
            self.model.dataChanged.emit(index,index)
            self.selectItems(index)


    def undo(self):
        for index,value in zip(self.indexes,self.prev_values):
            self.model.setData(index,value)
            self.model.dataChanged.emit(index,index)
            self.selectItems(index)



class CommandAddRow(QUndoCommand): #this is gonna be tough

    def __init__(self, parent, model, rows,description): #I've got an Idea
        """
        Method defines  Add Row to table
        Args:
             parent ()
             model (QModel*): Model reference for table
             rows (QIndex)  selected Rows
        """
        super(CommandAddRow, self).__init__(description)
        self.parent = parent
        self.model= model
        self.rows = rows
        self.rowCount  = self.model.rowCount()
        self.sortIndexes()

    def sortIndexes(self):
        temp_dict = {}
        for ind in self.rows:
            row = int(ind.row())
            temp_dict.update({ind:row})
        sorted_x = sorted(temp_dict.items(), key=operator.itemgetter(1))
        self.rows = [x[0] for x in sorted_x]



    def redo(self):
        if self.rowCount < 1:
            self.model.insertRow(0)
        else:
            count = 0
            for index in self.rows:
                row =  int(index.row())
                #print('row is ',row)
                self.model.insertRows(row+count) #-(count-1),count)
                count += 1





    def undo(self):
        count = 0
        for index in self.rows:
            row =  int(index.row())
            self.model.removeRows(row-count)



class CommandRemoveRow(QUndoCommand): #Fix row order

    def __init__(self, parent, model, rows,description): #I've got an Idea
        """
        Method defines  Remove Row to table
        Args:
             parent ()
             model (QModel*): Model reference for table
             rows (QIndex)  selected Rows
        """
        super(CommandRemoveRow, self).__init__(description)
        self.parent = parent
        self.model= model
        self.rows = rows
        self.pdb_rows = []
        self.sortIndexes()


    def sortIndexes(self):
        temp_dict = {}
        for ind in self.rows:
            #print('ind is ',ind)
            row = int(ind.row())
            temp_dict.update({ind:row})
        #print(temp_dict)
        sorted_x = sorted(temp_dict.items(), key=operator.itemgetter(1))
        #print('--'*20)
        #print(sorted_x)
        self.rows = [x[0] for x in sorted_x]

    def redo(self): #why what's the pronlem'
        count = 0
        for index in self.rows:
            row =  int(index.row())
            self.pdb_rows.append(self.model.getRow(row-count))
            self.model.removeRows(row-count) #-(count-1),count)
            count += 1

    def undo(self):
        #count = 0
        for index,row_data in zip(self.rows,self.pdb_rows):
            row =  int(index.row())
            #print('row is ',row)
            self.model.customInsertRows(row,row_data)

