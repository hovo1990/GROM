# -*- coding: utf-8 -*-
"""
    GROM.gro_model
    ~~~~~~~~~~~~~

    This is a custom model for  working with PDB files for QTableView  widget

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

import platform
import re
from PyQt5.QtCore import  (QModelIndex,QAbstractTableModel,
                           QSize, Qt, pyqtSignal)
from PyQt5.QtGui import (QColor, QTextDocument)
from PyQt5.QtWidgets import (QWidget, QTextEdit, QStyledItemDelegate, QUndoStack,
                             QUndoCommand, QComboBox,QSpinBox,QDoubleSpinBox,
                             QLineEdit)
#import richtextlineedit


from .undoCommands import CommandElementChange
import tableWidget.GRO_parse as GRO_parse


comitDataSignal = pyqtSignal(QWidget , name = "commitData" )
closeEditorSignal = pyqtSignal(QWidget, name = "closeEditor")



try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str

(residNum, residName, atomName, atomNum, X,Y,Z ) = range(7)



MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1


AMINOACID_COLORS = {'ALA':[200,200,200],
                    'ARG':[20,90,255],
                    'ASN':[0,220,220],
                    'ASP':[230,10,10],
                    'CYS':[230,230,0],
                    'GLN':[0,220,220],
                    'GLU':[230,10,10],
                    'GLY':[235,235,235],
                    'HIS':[130,130,210],
                    'ILE':[15,130,15],
                    'LEU':[15,130,15],
                    'LYS':[20,90,255],
                    'MET':[230,230,0],
                    'PHE':[50,50,170],
                    'PRO':[220,150,130],
                    'SER':[250,150,0],
                    'THR':[250,150,0],
                    'TRP':[180,90,180],
                    'TYR':[50,50,170],
                    'VAL':[15,130,15],
                    'ASX':[255,105,180],
                    'GLX':[255,105,180],
                    'other':[190,160,110]}


class GRO_rowInfo(object):


    def __init__(self, residNum,residNum_color,residName,residName_color,atomName, atomNum,X,Y,Z):
        """
        Method defines a single row of a gro format file

        Args:
             residNum (int) residue number (5 positions, integer)
             residNum_color (QColor)
             residueName (str) residue name (5 characters)
             residueName_color (QColor)
             atomName (str) atom name (5 characters)
             atomNum (int) atom number
             X (float) Orthogonal coordinates for X in Angstroms.
             Y (float) Orthogonal coordinates for Y in Angstroms.
             Z (float) Orthogonal coordinates for Z in Angstroms.
        """
        self.residNum = residNum
        self.residNum_initial  = residNum
        self.residNum_color = residNum_color
        self.residNum_color_initial = residNum_color
        self.residName = residName
        self.residName_color = residName_color
        self.atomName = atomName
        self.atomNum = atomNum
        self.X = X
        self.Y = Y
        self.Z = Z
        self.access = {0:self.residNum, 1:self.residName, 2:self.atomName, 3:self.atomNum,
                       4:self.X, 5:self.Y,6:self.Z}

    def __hash__(self):
        return super(GRO_rowInfo, self).__hash__()


    def __lt__(self, other):
        return self.name.lower() < other.name.lower()


    def __eq__(self, other):
        return self.name.lower() == other.name.lower()


class GRO_Container(object):

    def __init__(self, filename=""):
        self.filename = filename
        self.dirty = False
        self.GRO_ROWS = {}


    def GRO(self, identity):
        return self.GRO_ROWS.get(identity)



    def __len__(self):
        return len(self.GRO_ROWS)


    def __iter__(self):
        for GRO_ROW in self.GRO_ROWS.values():
            yield GRO_ROW


    def inOrder(self):
        return sorted(self.GRO_ROWS.values())


    def load(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            self.mol = GRO_parse.groParse(self.filename)
            for row in self.mol:
                ATOM = row[0]
                serial = row[1]
                name = row[2]
                resName = row[3]
                ChainID = row[4]
                resNum = row[5]
                X = row[6]
                Y = row[7]
                Z = row[8]
                occupancy = row[9]
                charge = row[10]
                element = row[11]
                GROrow = GRO_rowInfo(ATOM, serial, name, resName,ChainID, resNum,X,Y,Z, occupancy, charge, element)
                self.PDB_ROWS[id(GROrow)] = GROrow
            self.dirty = False
        except IOError as e:
            exception = e



    def save(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for saving")
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


class GROTableModel(QAbstractTableModel): #This part is the ultimate important part



    def __init__(self, filename=""):
        """
        Method defines a custom Model for working with GRO file for Table Widget

        Args:
             filename (str) filename if opened
        """
        super(GROTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.GRO_rows = []
        self.resNum_temp = 1


    def getVal(self,row,column):
        val = self.GRO_rows[row].access[column]
        return val

    def sortByName(self):
        self.GRO_rows = sorted(self.GRO_rows)
        self.reset()


    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable)


    def data(self, index, role=Qt.DisplayRole):
        GRO_row = self.GRO_rows[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:   #(residNum, residName, atomName, atomNum, X,Y,Z ) = range(7)
            if column == residNum:
                return GRO_row.residNum
            elif column ==  residName:
                return GRO_row.residName
            elif column == atomName:
                return GRO_row.atomName
            elif column == atomNum:
                return GRO_row.atomNum
            elif column == X:
                return GRO_row.X
            elif column == Y:
                return GRO_row.Y
            elif column == Z:
                return GRO_row.Z
        elif role == Qt.BackgroundRole:
            if column == residNum:
                return  GRO_row.residNum_color
            elif column == residName:
                return GRO_row.residName_color
        elif role == Qt.TextColorRole:
            if column == X:
                return QColor(Qt.red)
            elif column == Y:
                return QColor(Qt.green)
            elif column == Z:
                return QColor(Qt.blue)
        return None


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft|Qt.AlignVCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == residNum:
                return 'residNum'
            elif section == residName: ###(residNum, residName, atomName, atomNum, X,Y,Z ) = range(7)
                return 'residName'
            elif section == atomName:
                return 'atomName'
            elif section == atomNum:
                return 'atomNum'
            elif section == X:
                return 'X'
            elif section == Y:
                return 'Y'
            elif section == Z:
                return 'Z'
        return int(section + 1)



    def rowCount(self, index=QModelIndex()):
        return len(self.GRO_rows)


    def columnCount(self, index=QModelIndex()):
        return 7


    def setData(self, index, value, role=Qt.EditRole):
        """
        Method defines for setting up Data

        Args:
             index (QIndex*) index of the model
             value (str) modifies value at current selected index
        """
        if index.isValid() and 0 <= index.row() < len(self.GRO_rows):
            GRO_row = self.GRO_rows[index.row()]
            column = index.column()
            if column == residNum: # (residNum, atomName, atomNum, X,Y,Z ) = range(6)
                 GRO_row.residNum = int(value)
                 if int(GRO_row.residNum_initial) != int(GRO_row.residNum):
                     GRO_row.residNum_color = QColor(255,165,0)
                 else:
                     GRO_row.residNum_color = GRO_row.residNum_color_initial
            elif column == residName:
                GRO_row.residName = value
                if value in AMINOACID_COLORS:
                    Col = AMINOACID_COLORS[value]
                    GRO_row.residName_color = QColor(Col[0],Col[1],Col[2])
                else:
                    Col = AMINOACID_COLORS['other']
                    GRO_row.residName_color = QColor(Col[0],Col[1],Col[2])
            elif column ==  atomName:
                 GRO_row.atomName = value
            elif column ==  atomNum:
                 GRO_row.atomNum = int(value)
            elif column == X:
                 GRO_row.X = float(value)
            elif column == Y:
                 GRO_row.Y = float(value)
            elif column == Z:
                 GRO_row.Z = float(value)
            self.dirty = True
            self.dataChanged.emit(index,index)
            return True
        return False


    def getRow(self,position):
        return self.GRO_rows[position]


    def customInsertRows(self, position, row_data,rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.GRO_rows.insert(position + row,row_data)
        self.endInsertRows()
        self.dirty = True
        return True

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.GRO_rows.insert(position + row,
                              GRO_rowInfo("Unknown", "Unknown","Unknown"," Unknown",
                                          "Unknown"," Unknown", " Unknown"," Unknown"," Unknown",))
        self.endInsertRows()
        self.dirty = True
        return True  #(residNum, residName, atomName, atomNum, X,Y,Z ) = range(7)


    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.GRO_rows = (self.GRO_rows[:position] +
                      self.GRO_rows[position + rows:])
        self.endRemoveRows()
        self.dirty = True
        return True



    def load(self,fname): #This parts need modification
        self.filename = fname
        exception = None
        fh = None
        try:
            if self.filename != '':
                if not self.filename:
                    raise IOError("no filename specified for loading")
                self.GRO_rows = []
                self.molTotal = GRO_parse.groParse(self.filename)
                self.mol = self.molTotal[2:-1]
                #print('self.mol is ',self.mol)
                self.flag_color = True
                self.val = int(self.mol[2][0])
                for row in self.mol:
                    residNum = row[0]
                    if self.val != int(residNum):
                            if self.flag_color == True:
                                self.flag_color = False
                                #self.val = int(resNum)
                                residNum_color = QColor(Qt.green)
                            elif self.flag_color == False:
                                self.flag_color = True
                                #self.val = int(GRO_row.resNum)
                                residNum_color = QColor(Qt.yellow)
                            self.val = int(residNum)
                    elif self.flag_color == True and self.val == int(residNum):
                        residNum_color = QColor(Qt.yellow)
                    elif self.flag_color == False and self.val == int(residNum):
                        residNum_color = QColor(Qt.green)
                    residName = row[1]
                    if residName in AMINOACID_COLORS:
                        Col = AMINOACID_COLORS[residName]
                        residName_color = QColor(Col[0],Col[1],Col[2])
                    else:
                        Col = AMINOACID_COLORS['other']
                        residName_color = QColor(Col[0],Col[1],Col[2])
                    atomName = row[2]
                    atomNum = row[3]
                    X = row[4]
                    Y = row[5]
                    Z = row[6]
                    GROrow = GRO_rowInfo(residNum,residNum_color, residName,residName_color, atomName, atomNum, X,Y,Z )
                    self.GRO_rows.append(GROrow)
                    self.dirty = False
                    #self.extractInitData() #For test Purpose
        except IOError as e:
                exception = e
        finally:
                if fh is not None:
                    fh.close()
                if exception is not None:
                    raise exception

    def extractInitData(self):
        dataToSave = [self.molTotal[0],self.molTotal[1],self.molTotal[-1]]
        #print('self.dataToSave is ',self.dataToSave)
        return dataToSave



    def save(self,filename): #WIP
        self.filename = filename
        exception = None
        open_file = None
        try:
            if not self.filename:
                raise IOError("no filename specified for saving")
            open_file = open(self.filename,'w')
            dataExtra = self.extractInitData()
            GRO_parse.write_extraData_to_GRO(open_file,dataExtra[0])
            GRO_parse.write_extraData_to_GRO(open_file,[str(self.rowCount())])
            for row in self.GRO_rows:
                residNum = row.residNum
                residName = row.residName   #(residNum, residName, atomName, atomNum, X,Y,Z ) = range(7)
                atomName = row.atomName
                atomNum = row.atomNum
                x = row.X
                y = row.Y
                z = row.Z
                line= [residNum, residName, atomName, atomNum, x,y,z]
                #print('line is ',line)
                GRO_parse.write_SingleLine_to_GRO(open_file,line)
            GRO_parse.write_vectorBox_to_GRO(open_file,dataExtra[2])
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if open_file is not None:
                open_file.close()
            if exception is not None:
                raise exception


class GRODelegate(QStyledItemDelegate):


    def __init__(self, parent=None):
        super(GRODelegate, self).__init__(parent)
        self.undoStack = QUndoStack(self) #This is for undo/redo




    def paint(self, painter, option, index):
            QStyledItemDelegate.paint(self, painter, option, index)


    def sizeHint(self, option, index):
        fm = option.fontMetrics
        if index.column() == residNum:
            return QSize(fm.width("9,999,999"), fm.height())
        if index.column() == residName:
            text = index.model().data(index)
            document = QTextDocument()
            document.setDefaultFont(option.font)
            document.setHtml(text)
            return QSize(document.idealWidth() + 5, fm.height())
        return QStyledItemDelegate.sizeHint(self, option, index)


    def createEditor(self, parent, option, index): #residNum,residNum_color, residName, atomName, atomNum, X,Y,Z
        if index.column() == residNum:
            spinbox = QSpinBox(parent)
            spinbox.setRange(1, 200000)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        elif index.column() == residName:
            combobox = QComboBox(parent)
            combobox.addItems(list(AMINOACID_COLORS.keys()))
            combobox.setEditable(True)
            return combobox
        elif index.column() == atomName:
            editor = QLineEdit(parent)
            editor.returnPressed.connect(self.commitAndCloseEditor)
            return editor
        elif index.column() == atomNum:
            spinbox = QSpinBox(parent)
            spinbox.setRange(1, 200000)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        elif index.column() in (X,Y,Z): ###this works
            dspinbox = QDoubleSpinBox(parent)
            dspinbox.setRange(-200000, 200000)
            dspinbox.setSingleStep(0.1)
            dspinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return dspinbox
        else:
            return QStyledItemDelegate.createEditor(self, parent, option,
                                                    index)




    def commitAndCloseEditor(self):
        editor = self.sender()
        if isinstance(editor, (QTextEdit, QLineEdit)):
            comitDataSignal.emit(editor)
            closeEditorSignal .emit(editor)




    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        if  index.column() == residNum:
            if text is None:
                value = 0
            elif isinstance(text, int):
                value = text
            else:
                value = int(re.sub(r"[., ]", "", text))
            editor.setValue(value)
        #elif index.column() == residName:
            #editor.setText(text)
        elif index.column() == atomName:
            editor.setText(text)
        elif  index.column() == atomNum:
            if text is None:
                value = 0
            elif isinstance(text, int):
                value = text
            else:
                value = int(re.sub(r"[., ]", "", text))
            editor.setValue(value)
        elif  index.column() in (X,Y,Z):
            if text is None:
                value = 0
            elif isinstance(text, int):
                value = text
            else:
                value = float( text)
            editor.setValue(value)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):
        command = CommandElementChange(self, editor, model, index,
                             "Change item value")
        self.undoStack.push(command)
